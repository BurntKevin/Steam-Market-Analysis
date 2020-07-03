"""
Steam's API
    Output of Data
        Prices are in USD and is the median sale price for a given period
        Times are in UTC

Obtain Items
    Links
        API: https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}

Price History
    Data
        Obtain all historical data
        1 hour per point for one month ago
        1 day per point for more than one month ago
    Links
        API (but requires login cookie): https://steamcommunity.com/market/pricehistory/?appid={app_id}&market_hash_name={market_hash_name}
        Scrape: https://steamcommunity.com/market/listings/{app_id}/{market_hash_name}

Current Data
    Data
        Obtain's current instant buy price along with volume and median price of hour
    Links
        API (Best Instant Buy, Best Instant Sell, Pending Orders): https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}}
            For example https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid=175930085
        API (Used for Last 24 Hour Volume): https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_hash_name}

Get All Games
    Links
        API: http://api.steampowered.com/ISteamApps/GetAppList/v0002

General Issues to Consider
    No Price
        Some items do not have a price on Steam due to low volume or prices beyond Steam Market's limit
"""

# Processing Data
from datetime import datetime
from re import findall
from ast import literal_eval
from dateutil import relativedelta

# Requesting Data
from requests import get
from json import loads
from time import sleep

# Saving Data
from sqlalchemy import Column, String, Integer, NUMERIC, DateTime, ForeignKey, create_engine
from sqlalchemy_utils import URLType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2 import OperationalError

# Monitoring
from reporting import log_issue, send_email, print_issue

# Efficiency
from threading import Thread

# Design of Database
BASE = declarative_base()

class Game(BASE):
    """
    Stores Game information
    """
    __tablename__ = "Game"

    app_id = Column(Integer, primary_key=True) # Game identification
    name = Column(String) # Game name
    icon = Column(URLType) # URL of icon, can be derived but saving for processing efficiency

class Item(BASE):
    """
    Stores Item information
    """
    __tablename__ = "Item"

    market_hash_name = Column(String, primary_key=True) # Identifier for item
    name = Column(String) # Name of item
    app_id = Column(Integer, ForeignKey(Game.app_id)) # Link to Game table
    icon = Column(URLType) # URL of icon, can be derived but saving for processing efficiency
    item_name_id = Column(Integer) # Used to get price order history

class CsgoItem(BASE):
    """
    Stores CSGO item information
    """
    __tablename__ = "CsgoItem"

    market_hash_name = Column(String, ForeignKey(Item.market_hash_name), primary_key=True) # Link to Item table
    collection = Column(String) # Item collection (The Clutch Collection, etc)
    classification = Column(String) # Item classification (Classified, Exotic, etc)
    item_type = Column(String) # Item type (AK-47, Sticker, etc)

class PriceDaily(BASE):
    """
    Official prices from Steam on a daily timeframe
    """
    __tablename__ = "PriceDaily"

    market_hash_name = Column(String, ForeignKey(Item.market_hash_name), primary_key=True) # Link to item
    time = Column(DateTime, primary_key=True) # Date of data
    median_price = Column(NUMERIC) # Median price
    volume = Column(Integer) # Volume of item

class PriceHourly(BASE):
    """
    Official prices from Steam on an hourly timeframe
    """
    __tablename__ = "PriceHourly"

    market_hash_name = Column(String, ForeignKey(Item.market_hash_name), primary_key=True) # Link to item
    time = Column(DateTime, primary_key=True) # Date of data
    median_price = Column(NUMERIC) # Median price
    volume = Column(Integer) # Volume of item

class PriceLive(BASE):
    """
    Unofficial prices from Steam where it is current data at a specific timeframe
    """
    __tablename__ = "PriceLive"

    market_hash_name = Column(String, ForeignKey(Item.market_hash_name), primary_key=True) # Link to item
    time = Column(DateTime, primary_key=True) # Date of data scrape start, can be wrong by a fair margin of a couple minutes
    sell_price = Column(NUMERIC, nullable=True) # Best instant sell price
    buy_price = Column(NUMERIC, nullable=True) # Best instant buy price
    median_price = Column(NUMERIC, nullable=True) # Median price
    volume = Column(Integer, nullable=True) # Volume of item for the past 24 hours
    sell_quantity = Column(Integer, nullable=True) # Amount of items being sell listed, within 10% of the sell_price
    buy_quantity = Column(Integer, nullable=True) # Amount of items being buy listed, within 10% of the buy_price
    total_sell_quantity = Column(Integer, nullable=True) # Amount of items being sell listed, may be slightly incorrect as Steam only gives max 100 previous price points
    total_buy_quantity = Column(Integer, nullable=True) # Amount of items being buy listed, may be slightly incorrect as Steam only gives max 100 previous price points

# Creating database
DB = create_engine("postgres://steamdata_admin:testtest@steamdata.cpl2ejcsikco.us-east-1.rds.amazonaws.com:5432/postgres")
SESSION = sessionmaker(DB)()
BASE.metadata.create_all(DB)

# Steam Scraper
class SteamScraper():
    """
    Scrapes the Steam Market for prices, volumes and spreads along with item information
    """
    def __init__(self):
        """
        Connection points for Scraper to upload the data
        """
        # Getting database connections
        self.database_connection = create_engine("postgres://steamdata_admin:testtest@steamdata.cpl2ejcsikco.us-east-1.rds.amazonaws.com:5432/postgres", pool_size=-1, max_overflow=-1)
        self.session = sessionmaker(self.database_connection)

        # Queue of items to commit
        self.queued_items = []
    def commit_check(self):
        """
        Commits if there are 100 items on queue
        """
        # Checking if there are 100 queued items
        if len(self.queued_items) >= 1000:
            # Committing since there are over 100 items
            # Processing transaction
            thread = Thread(target=self.commit)
            thread.start()
    def commit(self):
        """
        Runs a commit
        """
        # Getting items required for a commit
        items, self.queued_items = self.queued_items, []

        # Telling user of progress
        print_issue(f"Uploading {len(items)} new entries")

        # Committing if there are items to commit
        if items:
            # Committing to database
            try:
                # Adding items to commit
                con = self.session()
                for item in items:
                    con.add(item)

                #  Comitting items
                con.commit()
            except OperationalError as E:
                # Informing of issue
                send_email(f"Failed to commit {len(items)} item(s) due to {E}")

                # Saving items back for next commit
                for item in items:
                    self.queued_items.append(item)
            except Exception as E:
                # Informing of issue
                send_email(f"Failed to commit {len(items)} item(s) due to {E}")

                # Entering all items into a file for later submission
                for item in items:
                    # Getting item details
                    variables = vars(item)

                    # Obtaining insert information
                    entry = ""
                    ending = ""
                    for key in variables:
                        if key != "_sa_instance_state":
                            entry = f"{entry}{key}, "
                            ending = f"{ending}'{variables[key]}', "
                    entry = f"INSERT INTO public.\"{type(item).__name__}\" ({entry[:-2]}) VALUES ({ending[:-2]});"

                    # Saving insert statement for later use
                    log_issue("steam_scraper_data", entry)
            finally:
                # Closing off connection
                try:
                    con.close()
                except Exception as E:
                    log_issue("steam_scraper_data", f"commit\tdatabase\tcon={con}\tConnection could not be made|{E}")

        # Telling user of progress
        print_issue(f"Finished uploading {len(items)} new entries")
    def get_page(self, url):
        """
        Obtains data about a game and waits until unblocked if blocked
        Steam blocks requests after more than 20 requests in a given minute
        """
        # Logging internet activity
        log_issue("steam_scraper_activity", f"{url}\t", date=False, new_line=False)

        while True:
            # Delay by three seconds
            sleep(3)

            # Obtaining page - providing a cookie appears to show you are more trustworthy to Steam and hence, more leeway but it expires in a few days
            page = get(url, cookies={"steamLoginSecure": "76561198085956525%7C%7C76168FE601593D8BC8A176CE6D78AB298B6D19A5"})

            # Returning page if successful
            if page.status_code == 200:
                # Notifying user of success
                log_issue("steam_scraper_activity", "")

                # Page successfully obtained
                return page

            # An issue occured, handling issue
            if page.status_code != 429 and page.status != 500 and page.status != 502:
                # Handler for invalid URLs and other issues
                log_issue("steam_scraper_stack", f"get_page\turl_issue\turl={url}\tGot status_code {page.status_code}")
                log_issue("steam_scraper_activity", "")
                raise Exception("URL is invalid")

            # Notifying user of re-request
            log_issue("steam_scraper_activity", "!", date=False, new_line=False)
    def query_database(self, query):
        """
        Queries the database and at most three times
        """
        # Trying to execute query
        try:
            return self.database_connection.execute(query)
        except Exception as E:
            # Warning administrator of potential database issues
            send_email(f"Failed to run {query} on database due to {E}")
            print(f"{E}")
            raise Exception(f"Could not run query {query}")
    def query_column_string(self, query):
        """
        Requests a single column and turns the data into set
        """
        # Obtaining data
        try:
            result = self.query_database(query)
        except Exception as E:
            # An issue with the database
            log_issue("steam_scraper_stack", f"query_column_string\tdatabase\tquery={query}\tCould not run query\t{E}")
            raise Exception(f"Could not run query {query}")

        # Cleaning data
        result_set = set()
        for item in result:
            result_set.add(item[0])

        return result_set
    def query_column_datetime(self, query):
        """
        Obtains datetime column as a set
        """
        # Obtaining data
        try:
            dates = self.query_database(query)
        except Exception as E:
            # An issue with the database
            log_issue("steam_scraper_stack", f"query_column_datetime\tdatabase\tquery={query}\tCould not run query\t{E}")
            raise Exception("Could not run query {query}")

        # Cleaning data
        result = set()
        for date in dates:
            result.add(date[0])

        return result
    def game_entry(self, app_id, name):
        """
        Creates a database entry for a game
        """
        # Checking header image is valid
        try:
            self.get_page(f"https://steamcdn-a.akamaihd.net/steam/apps/{app_id}/header.jpg")
        except Exception as E:
            log_issue("steam_scraper_stack", f"game_entry\ticon\tapp_id={app_id},name={name}\tCould not get icon\t{E}")

        self.queued_items.append(Game(app_id=app_id, name=name, icon=f"https://steamcdn-a.akamaihd.net/steam/apps/{app_id}/header.jpg"))
    def clean_query(self, name):
        return name.replace("'", "''")
    def item_entry(self, market_hash_name, name, app_id, icon, icon_large=""):
        """
        Creates a new database entry for an item
        """
        # Choosing large if possible
        if icon_large == "":
            chosen_icon = f"https://steamcommunity-a.akamaihd.net/economy/image/{icon}"
        else:
            chosen_icon = f"https://steamcommunity-a.akamaihd.net/economy/image/{icon_large}"

        # Checking if the icon is an actual page
        try:
            self.get_page(chosen_icon)
        except Exception as E:
            log_issue("steam_scraper_stack", f"item_entry\ticon\tmarket_hash_name={market_hash_name},name={name},app_id={app_id},icon={icon},icon_large={icon_large}\tCould not get icon\t{E}")

        # Obtaining page
        try:
            page = self.get_page(f"https://steamcommunity.com/market/listings/{app_id}/{market_hash_name}")
        except Exception as E:
            log_issue("steam_scraper_stack", f"item_entry\tpage\tmarket_hash_name={market_hash_name},name={name},app_id={app_id},icon={icon},icon_large={icon_large}\tCould not get page\t{E}")
            raise Exception("Could not find page for {market_hash_name}, {name}, {app_id}, {icon}, {icon_large}")

        # Parsing for item_name_id
        try:
            soup = page.text
            soup = findall(r"Market_LoadOrderSpread\( [0-9]* \)", soup)
            soup = soup[0].split(" ")
            item_name_id = soup[1]

            # Veryifying item_name_id
            try:
                self.get_page(f"https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}")
            except Exception as E:
                log_issue("steam_scraper_stack", f"item_entry\turl\tmarket_hash_name={market_hash_name},name={name},app_id={app_id},icon={icon},icon_large={icon_large},item_name_id={item_name_id}\tCould not get page\t{E}")
        except Exception as E:
            log_issue("steam_scraper_stack", f"item_entry\tpage\tmarket_hash_name={market_hash_name},name={name},app_id={app_id},icon={icon},icon_large={icon_large}\tould not get item_name_id")
            raise Exception("Could not find item_name_id for {market_hash_name}, {name}, {app_id}, {icon}, {icon_large}\t{E}")

        # Adding item
        self.queued_items.append(Item(market_hash_name=market_hash_name, name=name, app_id=app_id, icon=chosen_icon, item_name_id=item_name_id))
    def scan_for_new_items(self, app_id):
        """
        Scans the Steam market for new items and adds the unseen items
        """
        # Tracker for progress
        start = 0
        count_of_items = float("inf")
        try:
            saved_items_and_games = self.query_column_string('SELECT market_hash_name from Public."Item"')
            saved_items_and_games.update(self.query_column_string('Select app_id from Public."Game"'))
        except Exception as E:
            log_issue("steam_scraper_stack", f"scan_for_new_items\tdatabase\t\tCould not obtain saved_items_and_games\t{E}")
            raise Exception("Could not find obtain saved_items_and_games")

        # While there are still more items to obtain
        while start < count_of_items:
            # Obtaining page
            try:
                # Obtaining page information
                page = self.get_page(f"https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}")
                page = page.content
                page = loads(page)
            except Exception as E:
                log_issue(f"steam_scraper_stack", f"scan_for_new_items\turl\turl=https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}\tCould not get page\t{E}")
                continue

            # Adding all items on page
            try:
                # For all items on the page
                for item in page["results"]:
                    try:
                        # Obtaining potential new game
                        if item["asset_description"]["appid"] not in saved_items_and_games:
                            # New game found
                            self.game_entry(app_id=item["asset_description"]["appid"], name=item["app_name"])
                            saved_items_and_games.add(item["asset_description"]["appid"])

                        # Obtaining potential new item
                        if item["asset_description"]["market_hash_name"] not in saved_items_and_games:
                            # New item found
                            self.item_entry(item["asset_description"]["market_hash_name"], item["name"], item["asset_description"]["appid"], item["asset_description"]["icon_url"], item["asset_description"]["icon_url_large"])
                            saved_items_and_games.add(item["asset_description"]["market_hash_name"])
                    except Exception as E:
                        log_issue("steam_scraper_stack", f"scan_for_new_items\tpage\titem={item}\tCould not access json\t{E}")

                # Iterating to next count
                count_of_items = page["total_count"]
                start += 100
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_new_items\tpage\turl=https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}\tCould not access json\t{E}")

            # Checking if a commit is required
            self.commit_check()

        # Finishing off task
        self.commit()
    def scan_for_new_official_prices(self):
        """
        Scan for new prices of items (hourly and daily) and updates the database
        """
        def get_item_app_id_and_market_hash_name():
            """
            Obtains app_id and market_hash_name of all items
            """
            # Getting all known items
            try:
                # items = saved_items_add_games = self.query_column_string('SELECT app_id, market_hash_name FROM public."Item" where not exists (select market_hash_name from public."PriceDaily" WHERE public."PriceDaily".market_hash_name=public."Item".market_hash_name)')
                items = self.query_database('SELECT app_id, market_hash_name FROM public."Item" where not exists (select market_hash_name from public."PriceDaily" WHERE public."PriceDaily".market_hash_name=public."Item".market_hash_name)')
            except Exception as E:
                # Issue with database
                log_issue("steam_scraper_stack", f"get_item_app_id_and_market_hash_name\tdatabase\t\tCould not run query\t{E}")
                raise Exception("Could not obtain app_id, market_hash_name")

            # Cleaning data
            result = []
            for item in items:
                result.append((item[0], item[1]))

            return result
        # Obtaining known items
        try:
            items = get_item_app_id_and_market_hash_name()
        except Exception as E:
            # Issue with getting items
            log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\t\tCould not get item_app_id and market_hash_name\t{E}")
            raise Exception("Could not obtain app_id, market_hash_name")

        # Looking for prices for all items
        for item in items:
            # Obtaining page - not using API as that requires a cookie which expires within a couple days
            try:
                page = self.get_page(f"https://steamcommunity.com/market/listings/{item[0]}/{item[1]}")
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_new_official_prices\turl\turl=https://steamcommunity.com/market/listings/{item[0]}/{item[1]}\tCould not get page\t{E}")
                continue

            # Filtering page to useful data
            try:
                soup = findall(r"var line1=.*", page.text)
                history = literal_eval(soup[0][10:-2])
            except Exception as E:
                # Issue occurred, logging
                log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tpage\tpage={page}\tCould not access elements\t{E}")
                continue

            # Obtaining price points already added
            try:
                hourly_prices = self.query_column_datetime(f"SELECT time from public.\"PriceHourly\" where market_hash_name='{self.clean_query(item[1])}'")
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\t\tCould not get hourly prices\t{E}")
                continue
            try:
                daily_prices = self.query_column_datetime(f"SELECT time from public.\"PriceDaily\" where market_hash_name='{self.clean_query(item[1])}'")
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\t\tCould not get daily prices\t{E}")
                continue

            # Getting last month's date
            last_month = datetime.utcnow() - relativedelta.relativedelta(months=1)

            # For all prices
            for point in history:
                try:
                    point_date = datetime.strptime(point[0][:14], "%b %d %Y %H")
                except Exception as E:
                    log_issue("steam_scraper_stack", f"scan_for_new_official_prices\tdatabase\tpoint={point}\tCould not access elements\t{E}")
                    continue

                # Checking if point belongs to hourly or daily
                if last_month <= point_date:
                    # Hourly point
                    if point_date not in hourly_prices:
                        # New point
                        self.queued_items.append(PriceHourly(market_hash_name=item[1], time=point_date, median_price=point[1], volume=point[2]))
                else:
                    # Daily point
                    if point_date not in daily_prices:
                        # New point
                        self.queued_items.append(PriceDaily(market_hash_name=item[1], time=point_date, median_price=point[1], volume=point[2]))

            # Checking if a commit is required
            self.commit_check()

        # Finishing off task
        self.commit()
    def scan_for_live_prices(self):
        """
        Obtain's unofficial but detailed information for database
        """
        def get_item_app_id_and_market_hash_name_and_item_name_id():
            """
            Obtains app_id and market_hash_name of all items
            """
            # Getting all known items
            try:
                items = self.query_database('SELECT app_id, market_hash_name, item_name_id from Public."Item"')
            except Exception as E:
                log_issue("steam_scraper_stack", "get_item_app_id_and_market_hash_name_and_item_name_id\tdatabase\t\tCould not query\t{E}")
                raise Exception("Could not obtain app_id, market_hash_name, item_name_id")

            # Cleaning data
            result = []
            for item in items:
                result.append((item[0], item[1], item[2]))

            return result
        # Obtaining known items
        try:
            items = get_item_app_id_and_market_hash_name_and_item_name_id()
        except Exception as E:
            # Issue with obtaining values
            log_issue("steam_scraper_stack", f"scan_for_live_prices\tdatabase\t\tCould not query\t{E}")
            raise Exception("Could not obtain app_id, market_hash_name, item_name_id")

        # Looking for prices for all items
        for item in items:
            # Obtaining approximate time of scrape initation
            time = datetime.utcnow()

            # Obtaining buy order page
            try:
                page = self.get_page(f"https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item[2]}")
                page = page.content
                page = loads(page)
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tpage\turl=https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item[2]}\tCould not get page\t{E}")
                continue

            # Obtaining current bid and ask
            try:
                if page["sell_order_summary"] == "There are no active buy orders for this item.":
                    # There is currently no one buying
                    buy_price = None
                else:
                    # There is currently a price
                    buy_price = float(page["lowest_sell_order"]) / 100
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - lowest_sell_order\t{E}")
                continue
            try:
                if page["buy_order_summary"] == "There are no active buy orders for this item.":
                    # There is currently no one buying
                    sell_price = None
                else:
                    # There is currently a buyer
                    sell_price = float(page["highest_buy_order"]) / 100
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - highest_buy_order\t{E}")
                continue

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
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - buy_order_graph\t{E}")
                continue

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
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - sell_order_graph\t{E}")
                continue

            # Obtaining total items being sold and desired to be bought
            try:
                if page["sell_order_summary"] == "There are no active buy orders for this item.":
                    # No buying demand
                    total_buy_quantity = 0
                else:
                    # There are buyers
                    total_buy_quantity = findall(">[0-9]*<", page["sell_order_summary"])[0][1:-1]
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json array - sell_order_graph\t{E}")
                continue
            try:
                if page["buy_order_summary"] == "There are no active buy orders for this item.":
                    # No sell demand
                    total_sell_quantity = 0
                else:
                    # There are people selling
                    total_sell_quantity = findall(">[0-9]*<", page["buy_order_summary"])[0][1:-1]
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json array - buy_order_graph\t{E}")
                continue

            # Obtaining overview page
            try:
                page = self.get_page(f"https://steamcommunity.com/market/priceoverview/?appid={item[0]}&market_hash_name={item[1]}")
                page = page.content
                page = loads(page)
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\turl\turl=https://steamcommunity.com/market/priceoverview/?appid={item[0]}&market_hash_name={item[1]}\tCould not get page\t{E}")
                continue

            # Obtaining median price - can not be there if no volume
            try:
                median_price = page["median_price"][1:]
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - median_price\t{E}")
                median_price = None

            # Obtaining volume - can not be there if no volume
            try:
                # Obtaining volume and turning comma separated number into a number
                volume = page["volume"].replace(",", "")
            except Exception as E:
                log_issue("steam_scraper_stack", f"scan_for_live_prices\tjson\tpage={page}\tCould not access json - volume\t{E}")
                volume = None

            # Adding new point
            self.queued_items.append(PriceLive(market_hash_name=item[1], time=time, sell_price=sell_price, buy_price=buy_price, median_price=median_price, volume=volume, sell_quantity=sell_quantity, buy_quantity=buy_quantity, total_sell_quantity=total_sell_quantity, total_buy_quantity=total_buy_quantity))

            # Checking if a commit is required
            self.commit_check()

        # Finishing off task
        self.commit()
