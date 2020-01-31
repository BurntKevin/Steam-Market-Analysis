"""
Functions to allow access to the database easier
"""
from back_end.data.models import Game as db_game, Item as db_item, PriceHistoryPoint as db_pricehistorypoint
from back_end.scraper.scraper_data import Game as sc_game, Item as sc_item, PriceHistoryPoint as sc_pricehistorypoint
from sqlalchemy import desc
import datetime
from back_end.data.support import merge_sort

def upload_game_data(database, data):
    # Deleting game if exists
    db_game.query.filter_by(game_id=data.game_id).delete()

    # Adding game
    game_addition = db_game(game_id=data.game_id)
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
            price_addition = db_pricehistorypoint(date=price.date, price=price.price, volume=price.volume, item_name=item.name)
            database.session.add(price_addition)

    # Finalising
    database.session.commit()

def retrieve_game_data(game_id):
    # Creating game to return
    game_data = sc_game(game_id)

    # Retrieving items and it's corresponding price
    items = db_item.query.filter_by(game_id=game_id)
    for item in items:
        # Adding item
        item_data = sc_item(item.name, item.icon)

        # Adding price history
        price_history = db_pricehistorypoint.query.filter_by(item_name=item.name)
        return_price_history = []
        for price_history_point in price_history:
            price_history_point_data = sc_pricehistorypoint(price_history_point.date, price_history_point.price, price_history_point.volume)

            return_price_history.append(price_history_point_data)
        item_data.add_price_history(return_price_history)

        game_data.add_item(item_data)

    return game_data

def retrieve_basic_game_data():
    # Obtaining games
    games = db_game.query.filter_by()

    # Cleaning up data
    game_data = []
    for game in games:
        game_detail = sc_game(game.game_id)
        game_data.append({
            "game_id": game_detail.game_id,
            "game_icon": game_detail.game_icon()
        })

    # Returning game data
    return game_data

def retrieve_basic_item_data_from_game(game_id):
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

def retrieve_item_price_history(item_name):
    # Obtaining price history
    price_history = db_pricehistorypoint.query.filter_by(item_name=item_name).order_by()
    history = []
    for price_history_point in price_history:
        history.append(sc_pricehistorypoint(price_history_point.date, price_history_point.price, price_history_point.volume).deobject())

    # Returning data
    return history

def retrieve_fully_filled_item_price_history(item_name):
    """
    Fills up all blank dates with a date, None price and 0 volume
    """
    # Obtaining price history
    price_history = retrieve_item_price_history(item_name)

    # Obtaining all possible dates
    dates = []
    # If there is no price history, no need to find all dates
    if len(price_history) != 0:
        start = price_history[0]["price_history_point_date"]
        end = datetime.datetime.today()
        while start <= end:
            dates.append(sc_pricehistorypoint(start, None, 0).deobject())
            start += datetime.timedelta(days=1)

    # Sorting
    all_dates = dates + price_history
    all_dates = merge_sort(all_dates)

    # Returning data
    return all_dates

def retrieve_item_price_history_analysis(item_name):
    # Obtaining price history
    price_history = retrieve_fully_filled_item_price_history(item_name)

    # Adding percentage change and turnover to price
    previous_price = None;
    for price_history_point in price_history:
        if previous_price == None:
            # First price cannot have a percentage_change
            price_history_point["price_history_point_percentage_change"] = None
            price_history_point["price_history_point_turnover"] = price_history_point["price_history_point_volume"] * price_history_point["price_history_point_price"]
            
            previous_price = price_history_point["price_history_point_price"]
        if price_history_point["price_history_point_volume"] == 0:
            # Date added as a fill
            price_history_point["price_history_point_percentage_change"] = None
            price_history_point["price_history_point_turnover"] = None
            
        else:
            # Price can have a percentage change
            price_history_point["price_history_point_percentage_change"] = round((price_history_point["price_history_point_price"] / previous_price - 1) * 100, 3)
            price_history_point["price_history_point_turnover"] = price_history_point["price_history_point_volume"] * price_history_point["price_history_point_price"]
            previous_price = price_history_point["price_history_point_price"]

    # Returning data
    return price_history[::-1]
