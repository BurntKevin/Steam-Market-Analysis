"""
Scraper data structure
Game contains game name, game id, items
Item contains name, icon url, price history
Price history contains date, median price, volume, rsi, macd, percentage change, turnover
"""
# Scraper Library
from back_end.scraper.application.scraper_support import get_game_name_from_id, sort_objects_by_date

# Standard library
from datetime import datetime, timedelta

# Game class
class Game:
    """
    Holds all the skin information by a particular game
    """
    def __init__(self, game_id, game_name=None):
        """
        Initialises Game with the id of the game and a list of the items in the
        game which will be filled out later
        """
        self.game_id = int(game_id)
        if game_name is None:
            self.name = get_game_name_from_id(self.game_id)
        else:
            self.name = game_name
        self.items = []
    def add_item(self, new_item):
        """
        Adds an item to the game if applicable
        """
        conflict_item = self.item_exist(new_item)
        if conflict_item is False:
            # Adding item as it does not already exist
            self.items.append(new_item)
        else:
            # Notifying user of failed add if item is different
            if new_item.price_history != conflict_item.price_history:
                print(f"Error: Tried to replace {conflict_item.show()} with {new_item.show()}")
    def item_exist(self, new_item):
        """
        Check if an item already exists by their name
        If item does exist, return the item
        """
        # Checking if item already exists
        for item in self.items:
            # Item exists
            if item.name == new_item.name:
                return item

        # Item does not exist
        return False
    def show(self):
        """
        Prints the game's id and it's corresponding items and hence price history
        """
        # Printing id
        print(self.game_id)
        for item in self.items:
            print(f"  {item.show()}")
    def item_count(self):
        """
        Returns the amount of items in a game
        """
        return len(self.items)
    def same(self, game):
        """
        Check that a game is equal to another game
        Does not check individual price history of items
        """
        # Checking game_name
        if self.name != game.name:
            return False

        # Checking game_id
        if self.game_id != game.game_id:
            return False

        # Checking items are the same
        # Valid range checking
        if len(self.items) != len(game.items):
            return False
        # Checking items are the same
        for i in range(len(self.items)):
            if self.items[i].same(game.items[i]) is False:
                return False

        # Same game details
        return True
    def deobject(self):
        """
        Turns game object into standard data structure
        """
        # Obtaining item deobject
        item_data = []
        for item in self.items:
            item_data.append(item.deobject())

        return {
            "game_id": self.game_id,
            "items": item_data
        }
    def game_icon(self):
        """
        Returns the official game artwork
        """
        return f"https://steamcdn-a.akamaihd.net/steam/apps/{self.game_id}/header.jpg"

# Item class
class Item:
    """
    Holds information about a specific skin
    """
    def __init__(self, name, icon):
        """
        A skin has a name, an icon link and it's corresponding price history
        """
        self.name = name
        self.icon = f"https://steamcommunity.com/economy/image/{icon}"
        self.price_history = []
    def add_price_history(self, price_history):
        """
        Adds the price history to a skin, overwriting previous
        Done as it is assumed that the given price history is always the latest
        due to the nature of the scraper api always obtaining the entire price
        history rather than segments
        """
        # Clearing history
        self.price_history = price_history
        self.full_price_history()

        # Adding basic analysis
        self.add_percentage_change()

        # Adding technical analysis to the price history
        self.add_rsi_analysis()
    def full_price_history(self):
        """
        Fills in a price history with all data points from the first purchase
        to the last purchase where each data point has a date and the rest are
        None values
        """
        # Obtaining all possible dates
        dates = []
        # If there is no price history, no need to find all dates
        if len(self.price_history) != 0:
            # Calculating points between dates
            start = self.price_history[0].date
            end = self.price_history[len(self.price_history) - 1].date

            # Generating points
            while start <= end:
                # Adding date if it does not currently exist
                if self.date_exists(start) is False:
                    dates.append(PriceHistoryPoint(start, None, 0))

                start += timedelta(days=1)
        self.price_history += dates
        # Sorting price history
        self.price_history = sort_objects_by_date(self.price_history)
    def add_percentage_change(self):
        """
        Fills in the price history's percentage change
        If there is no price for a day, the percentage change is None and the
        percentage change is calculated from the last sale price
        """    
        previous_price = None
        # Adding percentage change for all applicable price history points
        for point in self.price_history:
            # Checking if it is a valid point - has a previous price and
            # has a current price
            if previous_price is not None and point.price is not None:
                # Possible to change
                price_change = point.price / previous_price
                if price_change < 1:
                    # Price went down
                    point.percentage_change = 1 - price_change
                else:
                    # Price went up or stagnant
                    point.percentage_change = price_change - 1

            # Updating previous price if there was a price
            if point.price is not None:
                previous_price = point.price
    def date_exists(self, date):
        """
        Checks if a date already exists in the price history
        """
        # Checking all points
        for point in self.price_history:
            if point.date == date:
                return True

        # Date does not exist
        return False
    def add_rsi_analysis(self):
        """
        Adds rsi technical analysis to all price history points
        """
        # Obtaining rsi for each respective applicable data point
        for i in range(14, len(self.price_history)):
            self.calculate_rsi_for_point(i)
    def calculate_rsi_for_point(self, i):
        """
        Calculates the rsi for a point
        Uses the standard formula for the calcualtion of RSI with 14 data
        points 100 - (100 / (1 + average_gain / average_loss))
        """
        if i < 14:
            raise ValueError("Insufficient data points")

        # Obtaining previous 13 points
        points = self.price_history[i - 14:i + 1]

        # Obtaining average upward movement and average downward movement
        average_upward_movement = 0
        average_downward_movement = 0
        previous_price = None
        # Cycling through all points
        for point in points:
            # Passing points without a price
            if point.price is None:
                continue
            # Passing if a previous price has not been found
            if previous_price is None:
                # Found a previous price
                previous_price = point.price
                continue

            if previous_price < point.price:
                # An increase in price
                average_upward_movement += (point.price - previous_price) / 14
            elif previous_price > point.price:
                # A reduction in price
                average_downward_movement += abs((previous_price - point.price) / 14)

            # Obtaining new price
            previous_price = point.price

        # Obtaining RSI
        if average_downward_movement == 0:
            return 100
        self.price_history[i].rsi = 100 - (100 / (1 + average_upward_movement / average_downward_movement))
    def show(self):
        """
        Returns the name, icon and length of price history in a formatted
        fashion
        Choosing to not print out the entire price history as it is excessive
        amounts of information and relatively useless
        """
        return f"{self.name} has icon {self.icon} with {len(self.price_history)} price history points"
    def same(self, item):
        """
        Check if an item is the same
        """
        # Checking name
        if self.name != item.name:
            return False

        # Checking icon
        if self.icon != item.icon:
            return False

        # Range checking for price_history
        if len(self.price_history) != len(item.price_history):
            return False

        # Ensuring each price point is the same
        for i in range(len(item.price_history)):
            # Ensuring details are the same
            if self.price_history[i].same(item.price_history[i]) is False:
                return False

        # Same item details
        return True
    def deobject(self):
        """
        Turns item object into standard data structure
        """
        # Obtaining price history
        price_history_data = []
        for price_history_point in self.price_history:
            price_history_data.append(price_history_point.deobject())

        return {
            "item_name": self.name,
            "item_icon": self.icon,
            "price_history": price_history_data
        }

# Price history point class
class PriceHistoryPoint:
    """
    Holdings the financial information about a skin at a particular point in
    time
    """
    def __init__(self, date, price, volume, rsi=None, macd=None, percentage_change=None):
        """
        The history includes the date which the data is based on, a price,
        volume, rsi, macd, percentage change from previous day and turnover
        """
        self.date = date
        self.price = price
        self.volume = int(volume)
        self.rsi = rsi
        self.macd = macd
        self.percentage_change = percentage_change
        if volume != 0:
            # Point has a price
            self.turnover = price * int(volume)
        else:
            # Point does not have a price
            self.turnover = None
    def show(self):
        """
        Returns the date, price and volume for printing
        """
        return f"{self.date.day}/{self.date.month}/{self.date.year} has price {self.price} and volume {self.volume}"
    def same(self, point):
        """
        Checks if a price point is the same
        """
        # Checking date
        if self.date != point.date:
            return False

        # Checking price
        if self.price != point.price:
            return False

        # Checking volume
        if self.volume != point.volume:
            return False

        # Checking rsi
        if self.rsi != point.rsi:
            return False

        # Checking macd
        if self.macd != point.macd:
            return False

        # Checking percentage_change
        if self.percentage_change != point.percentage_change:
            return False

        # Checking turnover
        if self.turnover != point.turnover:
            return False

        # Same price point data
        return True
    def deobject(self):
        """
        Turns price history object into  standard data structure
        """
        return {
            "price_history_point_date": self.date,
            "price_history_point_price": self.price,
            "price_history_point_volume": self.volume,
            "price_history_point_rsi": self.rsi,
            "price_history_point_macd": self.macd,
            "price_history_point_percentage_change": self.percentage_change,
            "price_history_point_turnover": self.turnover
        }
