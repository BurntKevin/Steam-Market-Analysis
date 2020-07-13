"""
Obtains item information from the Steam Market such as item details or prices
"""
# Processing Data
from datetime import datetime
from dateutil import relativedelta
from re import findall
from ast import literal_eval

# Requesting Data
from requests import get
from json import loads
from time import sleep

# Obtaining Data
from steam_database import SteamDatabase

# Monitoring
from reporting import log_issue, print_issue

class SteamScraper:
    """
    Scrapes the Steam Market for prices, volumes and spread along with item information
    """
    def __init__(self):
        # Connection to database
        self.database = SteamDatabase()
        self.database.ping_database()

        # Cookie for scraping
        try:
            self.last_cookie_check = datetime.utcnow()
            self.cookie = None
            self.get_cookie()
        except:
            print_issue("Could not get cookie")
    def get_cookie(self):
        """
        Obtain's cookie for better access to pages
        """
        try:
            # Attempting to get cookie
            self.cookie = self.database.get_cookie()
            self.last_cookie_check = datetime.utcnow()
        except Exception as e:
            # Informing user
            log_issue("steam_scraper_stack", f"get_cookie\tdatabase\t\tCould not get cookie {e}")
            raise Exception("Unable to get cookie")
    def get_page(self, url):
        """
        Obtains data about a game and waits until unblocked if blocked
        Steam blocks requests after more than 20 requests in a given minute
        """
        # Logging internet activity
        log_issue("steam_scraper_activity", f"{url}\t", date=False, new_line=False)

        if self.last_cookie_check + relativedelta.relativedelta(days=0.3) < datetime.utcnow():
            try:
                self.cookie = self.get_cookie()
            except Exception as e:
                log_issue("steam_scraper_stack", f"get_page\tdatabase\t\tCoudl not get cookie {e}")

        while True:
            # Delay by three seconds
            sleep(3)

            # Obtaining page - providing a cookie appears to show you are more trustworthy to Steam and hence, more leeway but it expires in a few days
            page = get(url, cookies={"steamLoginSecure": self.cookie})

            # Returning page if successful
            if page.status_code == 200:
                # Placing a new line and dating the request
                log_issue("steam_scraper_activity", "")

                # Page successfully obtained
                return page

            # An issue occured, handling issue
            if page.status_code != 429 and page.status != 500 and page.status != 502:
                # Handler for invalid URLs and other issues
                log_issue("steam_scraper_stack", f"get_page\turl_issue\turl={url}\tGot status_code {page.status_code}")

                # Adding a new line to scraper activity page
                log_issue("steam_scraper_activity", "")
                raise Exception("URL is invalid")

            # Notifying user of re-request
            log_issue("steam_scraper_activity", "!", date=False, new_line=False)
    def solve_tasks(self):
        """
        Works through tasks
        """
        while True:
            # Obtaining tasks
            try:
                tasks = self.database.obtain_tasks()
            except Exception as e:
                log_issue("steam_scraper_stack", f"solve_tasks\tdatabase\t\tCould not obtain tasks {e}")
                continue

            # Solving the tasks
            for task in tasks:
                # Notifying user of progress
                print(task)

                try:
                    # Solving task
                    if task[2] == "New Items":
                        self.scan_for_new_items_all(task[1])
                    elif task[2] == "Official Price":
                        self.scan_for_new_official_prices(task[0], task[1])
                    elif task[2] == "Live Price":
                        self.scan_for_live_prices(task[0], task[1])
                    else:
                        log_issue("steam_scraper_stack", f"solve_tasks\tunknown\ttask={task}\tUnknown item")

                    # Successfully added new item
                    try:
                        self.database.update_task(task[0], task[1], task[2])
                    except Exception as e:
                        log_issue("steam_scraper_stack", f"solve_tasks\tdatabase\ttask={task}\tFailed to add completed task {e}")

                    # Checking if a commit is required
                    try:
                        self.database.commit_checker()
                    except Exception as e:
                        log_issue("solve_tasks\tdatabase\t\tFailed to check for commits")
                except Exception as e:
                    # Logging issue
                    log_issue("steam_scraper_stack", f"solve_tasks\tfunctions\ttask={task}\tFailed to complete task {e}")

                    # Trying to free item
                    try:
                        self.database.update_task(task[0], task[1], task[2], True)
                    except Exception as e:
                        log_issue("steam_scraper_stack", f"solve_tasks\tdatabase\ttask={task}\tFailed to let go of task {e}")

            # Updating database that this worker is still working
            self.database.ping_database()
    def scan_for_new_items_all(self, app_id):
        """
        Scans for new items for a given game which are not yet in the database
        """
        # Tracker for progress
        start = 0
        count_of_items = float("inf")

        # Obtaining already known items and games
        try:
            saved_items_and_games = set(self.database.query_database('SELECT market_hash_name FROM Public."Item"'))
            saved_items_and_games.update(self.database.query_database('SELECT app_id FROM Public."Game"'))
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_new_items_all\tdatabase\t\tCould not obtain saved items and games\t{e}")
            raise Exception("Could not find obtain saved_items_and_games")

        # While there are still more items to obtain
        while start < count_of_items:
            # Obtaining page
            try:
                # Obtaining page information
                page = self.get_page(f"https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}")
                page = page.content
                page = loads(page)
            except Exception as e:
                log_issue(f"steam_scraper_stack", f"scan_for_new_items_all\turl\turl=https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}\tCould not get page\t{e}")
                continue

            # Adding new items
            try:
                self.scan_for_new_items_page(page, saved_items_and_games)
            except Exception as e:
                log_issue("steam_scraper_stack", f"scan_for_new_items_all\tpage\turl=https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}\tCould not access json\t{e}")

            # Iterating to next count
            count_of_items = page["total_count"]
            start += 100
    def scan_for_new_items_page(self, page, saved_items_and_games):
        """
        Scans for item details given a page
        """
        # For all items on the page
        for item in page["results"]:
            try:
                # Obtaining potential new game
                if item["asset_description"]["appid"] not in saved_items_and_games:
                    # New game found
                    try:
                        # Testing if the image is possible to obtain
                        self.get_page(f"https://steamcdn-a.akamaihd.net/steam/apps/{item['asset_description']['appid']}/header.jpg")

                        # Adding new game
                        self.database.add_game(item["asset_description"]["appid"], item["app_name"], f"https://steamcdn-a.akamaihd.net/steam/apps/{item['asset_description']['appid']}/header.jpg")

                        # Confirming that game has been added
                        saved_items_and_games.add(item["asset_description"]["appid"])
                    except Exception as e:
                        log_issue("steam_scraper_stack", f"scan_for_new_items_page\ticon\tapp_id={item['asset_description']['appid']},name={item['app_name']}\tCould not get icon\t{e}")

                # Obtaining potential new item
                if item["asset_description"]["market_hash_name"] not in saved_items_and_games:
                    # New item found
                    # Adding new item
                    # Choosing large icon if possible
                    try:
                        # Obtaining icon
                        if item['asset_description']['icon_url_large'] == "":
                            icon = f"https://steamcommunity-a.akamaihd.net/economy/image/{item['asset_description']['icon_url']}"
                        else:
                            icon = f"https://steamcommunity-a.akamaihd.net/economy/image/{item['asset_description']['icon_url_large']}"

                        # Checking if page is real
                        self.get_page(icon)
                    except Exception as e:
                        log_issue("steam_scraper_stack", f"scan_for_new_items_page\tapp_id={item['asset_description']['appid']},name={item['app_name']}\tCould not get icon\t{e}")
                        raise Exception("Could not find page for icon")

                    # Obtaining market page as a test
                    try:
                        page = self.get_page(f"https://steamcommunity.com/market/listings/{item['asset_description']['appid']}/{item['asset_description']['market_hash_name']}")
                    except Exception as e:
                        log_issue("steam_scraper_stack", f"add_item\tpage\tmarket_hash_name={item['asset_description']['appid']},app_id={item['app_name']}\tCould not get page\t{e}")
                        raise Exception(f"Could not find market listing")

                    # Parsing for item_name_id
                    try:
                        # Obtaining item_name_id
                        soup = page.text
                        soup = findall(r"Market_LoadOrderSpread\( [0-9]* \)", soup)
                        soup = soup[0].split(" ")
                        item_name_id = soup[1]

                        # Veryifying item_name_id
                        try:
                            self.get_page(f"https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}")
                        except Exception as e:
                            log_issue("steam_scraper_stack", f"item_entry\turl\tmarket_hash_name={item['asset_description']['market_hash_name']},app_id={item['asset_description']['appid']},item_name_id={item_name_id}\tCould not get page\t{e}")
                    except Exception as e:
                        log_issue("steam_scraper_stack", f"item_entry\tpage\tmarket_hash_name={item['asset_description']['market_hash_name']},app_id={item['asset_description']['appid']}\tould not get item_name_id")
                        raise Exception(f"Could not find item_name_id for {item['asset_description']['market_hash_name']}, {item['asset_description']['appid']}")

                    # Adding newly obtained item
                    self.database.add_item(item["asset_description"]["market_hash_name"], item["name"], item["asset_description"]["appid"], icon, item_name_id)

                    # Confirming that game has been added
                    saved_items_and_games.add(item["asset_description"]["market_hash_name"])
            except Exception as e:
                log_issue("steam_scraper_stack", f"scan_for_new_items\tpage\titem={item}\tCould not access json\t{e}")
    def scan_for_new_official_prices(self, market_hash_name, app_id):
        """
        Scans for new prices of items which are not yet in the database and adds them
        """
        # Obtaining page if not given - not using API as that requires a cookie which expires within a couple days
        try:
            page = self.get_page(f"https://steamcommunity.com/market/listings/{app_id}/{market_hash_name}")
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_new_official_prices\turl\turl=https://steamcommunity.com/market/listings/{app_id}/{market_hash_name}\tCould not get page\t{e}")
            raise Exception("Could not get page")

        # Filtering page to useful data
        try:
            soup = findall(r"var line1=.*", page.text)
            history = literal_eval(soup[0][10:-2])
        except Exception as e:
            # Issue occurred, logging
            log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tpage\tpage={page}\tCould not access elements for historical prices\t{e}")
            raise Exception("Could not get price history")

        # Obtaining price points already added - daily
        try:
            hourly_prices = self.database.query_database(f"SELECT time from public.\"PriceHourly\" where market_hash_name='{self.database.clean_market_hash_name(market_hash_name)}'")
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\t\tCould not get hourly prices\t{e}")
            raise Exception("Could not get hourly prices")

        # Obtaining price points already added - hourly
        try:
            daily_prices = self.database.query_database(f"SELECT time from public.\"PriceDaily\" where market_hash_name='{self.database.clean_market_hash_name(market_hash_name)}'")
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\t\tCould not get daily prices\t{e}")
            raise Exception("Could not get daily prices")

        # Getting last month's date
        last_month = datetime.utcnow() - relativedelta.relativedelta(months=1)

        # For all prices
        for point in history:
            try:
                point_date = datetime.strptime(point[0][:14], "%b %d %Y %H")
            except Exception as e:
                log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\tpoint={point}\tCould not access elements for time\t{e}")
                continue

            # Checking if point belongs to hourly or daily
            if last_month <= point_date:
                # Hourly point
                if point_date not in hourly_prices:
                    # New point
                    self.database.add_price_hourly(market_hash_name, point_date, point[1], point[2])
            else:
                # Daily point
                if point_date not in daily_prices:
                    # New point
                    self.database.add_price_daily(market_hash_name, point_date, point[1], point[2])
    def scan_for_live_prices(self, market_hash_name, app_id):
        """
        Obtain's unofficial but detailed information about an item
        """
        # Obtaining item_name_id
        try:
            item_name_id = self.database.query_database(f"SELECT item_name_id FROM public.\"Item\" WHERE market_hash_name='{self.database.clean_market_hash_name(market_hash_name)}' AND app_id={app_id}")
            item_name_id = item_name_id[0]
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tdatabase\t\tCould not get item_name_id\t{e}")
            raise Exception("Could not get item name id")

        # Obtaining approximate time of scrape initation
        time = datetime.utcnow()

        # Obtaining buy order page
        try:
            page = self.get_page(f"https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}")
            page = page.content
            page = loads(page)
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tpage\turl=https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}\tCould not get page\t{e}")
            raise Exception("Could not get order page")

        # Obtaining current bid and ask
        try:
            if page["sell_order_summary"] == "There are no active listings for this item.":
                # There is currently no one buying
                buy_price = "NULL"
            else:
                # There is currently a price
                buy_price = float(page["lowest_sell_order"]) / 100
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - lowest_sell_order\t{e}")
            raise Exception("Could not get sell orders")
        try:
            if page["buy_order_summary"] == "There are no active buy orders for this item.":
                # There is currently no one buying
                sell_price = "NULL"
            else:
                # There is currently a buyer
                sell_price = float(page["highest_buy_order"]) / 100
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - highest_buy_order\t{e}")
            raise Exception("Could not get buy orders")

        # Obtaining reasonably priced sell quantity
        try:
            sell_quantity = 0

            # Going through all orders
            for sell_order in page["buy_order_graph"]:
                # Adding if the price meets condition, otherwise stop
                if sell_order[0] >= sell_price * 0.9:
                    sell_quantity += sell_order[1]
                else:
                    break
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - buy_order_graph\t{e}")
            raise Exception("Could not get buy orders reasonable")

        # Obtaining reasonably priced buy quantity
        try:
            buy_quantity = 0

            # Going through all orders
            for buy_order in page["sell_order_graph"]:
    
                # Adding quantity if the price meets condition, otherwise stop
                if buy_order[0] <= buy_price / 0.9:
                    buy_quantity += buy_order[1]
                else:
                    break
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - sell_order_graph\t{e}")
            raise Exception("Could not get sell orders reasonable")

        # Obtaining total items being sold and desired to be bought
        try:
            if page["sell_order_summary"] == "There are no active listings for this item.":
                # No buying demand
                total_buy_quantity = 0
            else:
                # There are buyers
                total_buy_quantity = findall(">[0-9]*<", page["sell_order_summary"])[0][1:-1]
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json array - sell_order_summary\t{e}")
            raise Exception("Could not get total items sold")
        try:
            if page["buy_order_summary"] == "There are no active buy orders for this item.":
                # No sell demand
                total_sell_quantity = 0
            else:
                # There are people selling
                total_sell_quantity = findall(">[0-9]*<", page["buy_order_summary"])[0][1:-1]
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json array - buy_order_graph\t{e}")
            raise Exception("Could not get total items bought")

        # Obtaining overview page
        try:
            page = self.get_page(f"https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_hash_name}")
            page = page.content
            page = loads(page)
        except Exception as e:
            log_issue("steam_scraper_stack", f"scan_for_live_prices\turl\turl=https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_hash_name}\tCould not get page\t{e}")
            raise Exception("Could not get overview page")

        # Obtaining median price - can not be there if no volume
        try:
            median_price = page["median_price"][1:].replace(",", "")
        except Exception as e:
            median_price = "NULL"

        # Obtaining volume - can not be there if no volume
        try:
            # Obtaining volume and turning comma separated number into a number
            volume = page["volume"].replace(",", "")
        except Exception as e:
            volume = "NULL"

        try:
            self.database.add_price_live(market_hash_name, time, sell_price, buy_price, median_price, volume, sell_quantity, buy_quantity, total_sell_quantity, total_buy_quantity)
        except Exception as e:
            raise Exception(f"Could not update database {e}")

# Activating steam scraper
if __name__ == "__main__":
    SCRAPER = SteamScraper()
    SCRAPER.solve_tasks()
