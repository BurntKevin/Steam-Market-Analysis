"""
Scraper data structure
Game contains game id, items
Item contains name, icon url, price_history
Price history contains date, median price, volume
"""
# Support Library
from datetime import datetime # Simplfying dates

# Game class
class Game:
    """
    Holds all the skin information by a particular game
    """
    def __init__(self, game_id):
        """
        Initialises Game with the id of the game and a list of the items in the
        game which will be filled out later
        """
        self.game_id = game_id
        self.items = []
    def add_item(self, new_item):
        """
        Adds an item to the game if applicable
        """
        conflict_item = self.item_exist(new_item)
        if conflict_item is False:
            # Adding item as it doesn't already exist
            self.items.append(new_item)
        else:
            # Notifying user of failed add if item is different
            if new_item.price_history != conflict_item.price_history:
                print("Error: Tried to replace {} with {}".format(conflict_item.show(), new_item.show()))
    def item_exist(self, new_item):
        """
        Check if an item already exists by their name
        If item does exist, return the item
        """
        # Checking if item already exists
        for item in self.items:
            if item.name == new_item.name:
                return item
        return False
    def show(self):
        """
        Prints the game's id and it's corresponding items
        """
        # Printing id
        print(self.game_id)
        for item in self.items:
            print("  {}".format(item.show()))
    def item_count(self):
        """
        Returns the amount of items in a game
        """
        return len(self.items)
    def same(self, game):
        """
        Check that a game is equal to another game
        """
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
        self.icon = "https://steamcommunity.com/economy/image/{}".format(icon)
        self.price_history = []
    def add_price_history(self, price_history):
        """
        Adds the price history to a skin
        """
        # Clearing history
        self.price_history = []

        # Adding history
        self.price_history.append(price_history)
    def show(self):
        """
        Returns the name, icon and length of price history in a formatted
        fashion
        Choosing to not print out the entire price history as it is excessive
        amounts of information and relatively useless
        """
        return "{} has icon {} with {} price history points".format(self.name, self.icon, len(self.price_history))
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

# Price history point class
class PriceHistoryPoint:
    """
    Holdings the financial information about a skin at a particular point in
    time
    """
    def __init__(self, date, price, volume):
        """
        The history includes the date which the data is based on, a price and
        its volume
        """
        self.date = datetime.strptime(date[0:11], "%b %d %Y")
        self.price = price
        self.volume = volume
    def show(self):
        """
        Returns the date, price and volume for printing
        """
        return "{}/{}/{} has price {} and volume {}".format(self.date.day, self.date.month, self.date.year, self.price, self.volume)
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

        # Same price point data
        return True
