"""
Scraper functions
Used to obtain information about items in the Steam Market - game, game id,
item name, item icon
"""
# Support Library
from datetime import datetime # To manage dates

# Scraper Library
from scraper_support import get_page, string_to_query_string
from scraper_data import Game, Item, PriceHistoryPoint

def get_item_count(game_id):
    """
    Finds the amount of items a game has
    """
    # Obtaining page content
    url = f"https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=100&appid={game_id}&start=0"
    page = get_page(url)

    # Finding total number of items
    total_items = page["total_count"]

    return total_items

def get_items_basic_details_from_page(game_id, start_position):
    """
    Finds the item name from a given render page
    """
    # Getting item page
    url = f"https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=100&appid={game_id}&start={start_position}"
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
    data = Game(game_id)
    total_items = get_item_count(game_id)
    for start_position in range(0, total_items + 50, 50):
        for item in get_items_basic_details_from_page(game_id, start_position):
            data.add_item(item)

    # Returning
    return data

def get_item_price_history_from_page(game_id, item):
    """
    Gets an item's latest price history
    """
    url = f"https://steamcommunity.com/market/pricehistory/?appid={game_id}&market_hash_name={string_to_query_string(item)}"

    # Obtaining prices
    page = get_page(url)

    # Checking status of get_page
    if page is None:
        # Unsuccessful price
        price_history = []
    else:
        # Successful price
        prices = page["prices"]

        # Obtaining price history
        price_history = []
        for price in prices:
            point = PriceHistoryPoint(datetime.strptime(price[0][0:11], "%b %d %Y"), price[1], price[2])
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
        item.add_price_history(get_item_price_history_from_page(game_id, item.name))

    return game

def get_item_details(item_name):
    """
    Gets an item's details
    """
    # Obtaining data
    data = get_page(f"https://steamcommunity.com/market/search/render/?norender=1&query={item_name}")

    new_data = []
    for item in data["results"]:
        # Creating game
        game_addition = Game(item["asset_description"]["appid"])

        # Obtaining item details
        item_addition = Item(item["asset_description"]["market_hash_name"], item["asset_description"]["icon_url"])
        item_addition.add_price_history(get_item_price_history_from_page(item["asset_description"]["appid"], item["asset_description"]["market_hash_name"]))
        game_addition.add_item(item_addition)

        new_data.append(game_addition)

    # Returning
    return new_data
