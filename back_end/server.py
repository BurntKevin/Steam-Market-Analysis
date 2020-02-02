"""
Server functions
"""

# Standard Libraries
from json import dumps
from flask import Blueprint, request

# Custom Libraries
from back_end.__init__ import DB, create_app
from back_end.scraper.application.scraper import get_items_price_history
from back_end.data.application.database import upload_game_data, retrieve_all_game_basic_data, retrieve_game_items_basic_data, retrieve_price_history_data

# Setting up server and database
MAIN = Blueprint("main", __name__)
DB.create_all(app=create_app())

# Server functions
@MAIN.route("/add_game", methods=["POST"])
def add_game():
    """
    Adds or updates a game to the latest information
    """
    # Obtaining request details
    game_data = request.get_json()

    # Getting game data to add
    game = get_items_price_history(game_data["gameId"])

    # Saving the game's details
    upload_game_data(DB, game)

    return "Done", 201

@MAIN.route("/view_games")
def all_game_basic_data():
    """
    Obtains basic game data for the user
    """
    # Getting all games
    games = retrieve_all_game_basic_data()

    # Returning data
    return {"games": games}

@MAIN.route("/view_game_items")
def game_items_basic_data():
    """
    Obtains basic item data for the user
    """
    # Obtaining item details
    game_id = request.args.get("game_id")[1:]
    items = retrieve_game_items_basic_data(game_id)

    # Returning data
    return {"items": items}

@MAIN.route("/view_item_price_history")
def item_price_history_data():
    """
    Obtains price history data
    """
    # Obtaining item details
    item_name = request.args.get("item_name")[1:]
    price_history = retrieve_price_history_data(item_name)

    # Transforming data for use
    data = []
    for price_history_point in price_history:
        data.append(price_history_point.deobject())

    # Returning data
    return {"price_history": data[::-1]}

@MAIN.route("/view_item_price_history_chart")
def item_price_history_data_for_chart():
    """
    Obtains information for chart
    """
    # Obtaining item details
    item_name = request.args.get("item_name")[1:]
    price_history = retrieve_price_history_data(item_name)

    # Transforming data for chart framework
    data = []
    for price_history_point in price_history:
        data.append([
            price_history_point.date.strftime('%m/%d/%Y %H:%M:%S'),
            price_history_point.price,
            price_history_point.volume,
            price_history_point.rsi
        ])

    # Returning data
    return {"price_history": data}
