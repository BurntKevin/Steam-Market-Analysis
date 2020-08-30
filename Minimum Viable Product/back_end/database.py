"""
Functions to allow access to the database easier
"""
# Data library
from models import Game as db_game, Item as db_item, PriceHistoryPoint as db_pricehistorypoint

# Scraper library
from scraper_data import Game as sc_game, Item as sc_item, PriceHistoryPoint as sc_pricehistorypoint

def upload_game_data(database, data):
    """
    Uploads game object to database
    Assumes game object is the latest version
    """
    # Deleting game if exists
    db_game.query.filter_by(game_id=data.game_id).delete()

    # Adding game
    game_addition = db_game(game_id=data.game_id, game_name=data.name)
    database.session.add(game_addition)

    # Uploading a game's item and it's price
    for item in data.items:
        # Deleting item if exists
        db_item.query.filter_by(name=item.name).delete()

        # Adding item
        item_addition = db_item(name=item.name, icon=item.icon, game_id=data.game_id)
        database.session.add(item_addition)
        for price in item.price_history:
            # Deleting price_history if exists
            db_pricehistorypoint.query.filter_by(date=price.date, item_name=item.name).delete()

            # Adding price
            price_addition = db_pricehistorypoint(date=price.date, price=price.price, volume=price.volume, rsi=price.rsi, macd=price.macd, percentage_change=price.percentage_change, turnover=price.turnover, item_name=item.name)
            database.session.add(price_addition)

    # Finalising
    database.session.commit()

def retrieve_game_data(game_id):
    """
    Obtains game details according to game data
    """
    # Creating game to return
    game_data = sc_game(game_id)

    # Retrieving items and it's corresponding price
    items = db_item.query.filter_by(game_id=game_id)
    for item in items:
        item_data = retrieve_item_data(item.name)

        game_data.add_item(item_data)

    return game_data

def retrieve_item_data(item_name):
    """
    Obtains item details according to item name
    """
    # Obtaining item
    item_database = db_item.query.filter_by(name=item_name)

    # Creating item
    item_data = sc_item(item_database.name, item_database.icon)

    # Adding price history
    price_history = retrieve_price_history_data(item_name)
    item_data.add_price_history(price_history)

    return item_data

def retrieve_price_history_data(item_name):
    """
    Obtain price history details according to item name
    """
    # Obtaining price history
    price_history = db_pricehistorypoint.query.filter_by(item_name=item_name).order_by()
    history = []
    for point in price_history:
        history.append(sc_pricehistorypoint(point.date, point.price, point.volume, point.rsi, point.macd, point.percentage_change))

    # Returning data
    return history

def retrieve_all_game_basic_data():
    """
    Obtains all game's name and icon
    """
    # Obtaining games
    games = db_game.query.filter_by()

    # Cleaning up data
    game_data = []
    for game in games:
        game_detail = sc_game(game.game_id, game.game_name)
        game_data.append({
            "game_name": game_detail.name,
            "game_id": game_detail.game_id,
            "game_icon": game_detail.game_icon()
        })

    # Returning game data
    return game_data

def retrieve_game_items_basic_data(game_id):
    """
    Obtain basic data about a game's item
    """
    # Obtaining items
    items = db_item.query.filter_by(game_id=game_id)

    # Cleaning up data
    item_data = []
    for item in items:
        item_data.append({
            "item_name": item.name,
            "item_icon": item.icon
        })

    # Returning data
    return item_data
