"""
Obtain's prices from CSGOEmpire and attempts to buy undervalued items and also
sell overvalued items when compared to the Steam Market
CSGOEmpire's pricing algorithm has flaws and hence, it is possible to profit
"""
from requests import get
from json import loads
from time import sleep
import datetime
from sys import stdout

class MarketMakingCSGOEmpire():
    """
    Finds undervalued and overvalued items to trade
    """
    def __init__(self):
        """
        Prices used to later display all information to user
        Collated data is used to quickly filter through redundant queries as
        the time to search is a major factor in speed
        """
        self.prices = []
        self.collated_data = {}
    def obtain_csgoempire_trade_locked_page_information(self):
        """
        Obtain's CSGOEmpire's Trade Locked page items
        """
        # Obtaining page
        response = get("https://csgoempire.com/api/v2/hermes/inventory/74")
        response = response.content
        response = loads(response)

        # Adding items to list of potential items
        self.collate_page_response(response)
    def obtain_csgoempire_trade_unlocked_page_information(self):
        """
        Obtain's CSGOEmpire's Instant Withdraw page items
        """
        # Obtaining page
        response = get("https://csgoempire.com/api/v2/p2p/inventory/test/1")
        response = response.content
        response = loads(response)

        # Adding items to list of potential items
        self.collate_page_response(response)
    def obtain_steam_price(self, app_id, item):
        """
        Obtain's the Steam price for each respective item
        """
        # Delay pings
        sleep(1)

        try:
            while True:
                # Obtaining page
                steam_page = get(f"https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={item}")

                # Checking if website is on cooldown
                if steam_page.status_code == 429:
                    # Steam blocks requests after more than 20 requests in a given minute
                    sleep(3)
                elif steam_page.status_code == 400:
                    # URL is wrong
                    return float('inf')
                else:
                    # Page successfully obtained
                    # Obtaining page details
                    steam_page = steam_page.content
                    steam_page = loads(steam_page)

                    # Checking if the item has a current price
                    if "lowest_price" not in steam_page:
                        # Result has no current price
                        return float('inf')

                    # Cleaning and returning data
                    return int(float(steam_page["lowest_price"].replace(",", "")[1:]) * 100)

                print(".", end="")
                stdout.flush()
        except:
            # Obtain URL which caused issues
            print(f"https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={item}")
            return float('inf')
    def collate_page_response(self, response):
        """
        Collapses items with the same price to reduce queries
        """
        # Cycling through responses
        for entry in response:
            # Adding response, minimum where possible to enduce a check
            if (entry["appid"], entry["market_name"]) in self.collated_data:
                self.collated_data[(entry["appid"], entry["market_name"])] = min(self.collated_data[(entry["appid"], entry["market_name"])], entry["market_value"])
            else:
                self.collated_data[(entry["appid"], entry["market_name"])] = entry["market_value"]
    def find_prices(self):
        """
        Finds undervalued and overvalued items on CSGOEmpire
        """
        # Obtaining items
        self.obtain_csgoempire_trade_unlocked_page_information()
        self.obtain_csgoempire_trade_locked_page_information()

        # Notifying user of expected required time
        print(f"There are {len(self.collated_data)} items and it will take about {len(self.collated_data) * 4} seconds which is {round(len(self.collated_data) * 4 / 60, 2)} minutes")

        # Cycling through items to find overvalued or undervalued
        for entry in self.collated_data.items():
            # Finding Steam price to compare with
            steam_price = self.obtain_steam_price(entry[0][0], entry[0][1])

            # Finding value amount
            percentage_discount = (steam_price - entry[1]) / steam_price

            # Notify user of progress as process is slow
            print(entry[1], steam_price, round(percentage_discount, 2), entry[0][1])

            # Adding item for later publishing
            self.prices.append((entry[1], steam_price, round(percentage_discount, 2), entry[0][1]))

        # Filtering data to sorted order for easier digestion
        self.prices.sort(key=lambda x:x[2])

        # Giving information to user
        print("=================")
        for entry in self.prices:
            print(entry)
