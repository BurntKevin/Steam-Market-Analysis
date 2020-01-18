"""
Scraper functions
Used to obtain information about items in the Steam Market - game, game id,
item name, item icon
"""
# Support Library
from os.path import exists # To check files

# Scraper Library
from scraper_support import list_duplicate_remover, data_from_pickle_file, get_page, string_to_query_string, get_file_location
from scraper_data import Game, Item, PriceHistoryPoint

def get_item_count(game_id):
    """
    Finds the amount of items a game has
    """
    # Obtaining page content
    url = "https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=100&appid={}&start=0".format(game_id)
    page = get_page(url)

    # Finding total number of items
    total_items = page["total_count"]

    return total_items

def get_items_basic_details_from_page(game_id, start_position):
    """
    Finds the item name from a given render page
    """
    # Getting item page
    url = "https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=100&appid={}&start={}".format(game_id, start_position)
    page = get_page(url)
    page = page["results"]

    # Obtaining item details
    items = []
    for item in page:
        items.append(Item(item["hash_name"], item["asset_description"]["icon_url"]))

    return items

def get_items_basic_details(game_id):
    """
    Adds a game's items
    """
    # Maximum load is 100 items per page
    # Looping by 50 items per page as it allows a buffer for the dynamic sorted
    # nature of the items being obtained
    total_items = get_item_count(game_id)
    items = []
    for start_position in range(0, total_items + 50, 50):
        items += get_items_basic_details_from_page(game_id, start_position)
    # Cleaning up duplicates in the items obtained
    items = list_duplicate_remover(items)

    # Checking if this is an update to items or if this is the first time
    file_location = get_file_location(game_id)
    if exists(file_location):
        # Checking for new additions to add
        data = data_from_pickle_file(file_location)
        # Adding new items
        for item in items:
            data.add_item(item) # Has a check so that only new items are added
    else:
        # Setting up data to be returned
        data = Game(game_id)
        for item in items:
            data.add_item(item)

    return data

def get_item_price_history_from_page(game_id, item):
    """
    Gets an item's latest price history
    """
    url = "https://steamcommunity.com/market/pricehistory/?appid={}&market_hash_name={}".format(game_id, string_to_query_string(item))

    # Obtaining prices
    page = get_page(url)
    prices = page["prices"]

    # Obtaining price history
    price_history = []
    for price in prices:
        point = PriceHistoryPoint(price[0][0:11], price[1], price[2])
        price_history.append(point)

    # Returning
    return price_history

def get_items_price_history(game_id):
    """
    Gets a game's item's price history
    """
    # Obtaining items
    game = get_items_basic_details(game_id)

    # Getting price history for each item
    for item in game.items:
        item.price_history = get_item_price_history_from_page(game_id, item.name)

    return game
