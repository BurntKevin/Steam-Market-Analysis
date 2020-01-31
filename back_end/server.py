# Standard Libraries
from flask import Blueprint, jsonify, request, redirect, url_for

# Custom Libraries
from back_end.__init__ import db, create_app
from back_end.data.models import Game, Item, PriceHistoryPoint
from back_end.scraper.scraper import get_items_price_history
from back_end.data.database import upload_game_data, retrieve_game_data, retrieve_basic_game_data, retrieve_basic_item_data_from_game, retrieve_item_price_history, retrieve_fully_filled_item_price_history, retrieve_item_price_history_analysis
from back_end.technical_analysis.technical_analysis import calculate_rsi_from_price_history

from json import dumps

# Setting up server and database
main = Blueprint("main", __name__)
db.create_all(app=create_app())

# Server functions
@main.route("/add_game", methods=["POST"])
def add_game():
    """
    Adds or updates a game to the latest information
    """
    # Obtaining request details
    game_data = request.get_json()

    # Getting game data to add
    game = get_items_price_history(game_data["gameId"])

    # Converting game's details into a commit
    upload_game_data(db, game)

    return "Done", 201

@main.route("/basic_game_data")
def basic_game_data():
    # Getting all games
    games = retrieve_basic_game_data()

    # Returning data
    return {"games": games}

@main.route("/view_all_items")
def view_all_items():
    # Obtaining item details
    game_id = request.args.get("game_id")[1:]
    items = retrieve_basic_item_data_from_game(game_id)

    # Returning data
    return {"items": items}

@main.route("/view_item_price_history_chart")
def view_item_price_history_chart():
    # Obtaining item details
    item_name = request.args.get("item_name")[1:]
    price_history = retrieve_fully_filled_item_price_history(item_name)
    # price_history = calculate_rsi_from_price_history(price_history)

    """
    MAJOR PROBLEMM!!!! FUNCTION OR FUNCTION CALLER DOES NOT WORK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! PROPERLY TODO
    """

    # Transforming data for chart framework
    data = []
    for price_history_point in price_history:
        data.append([
            price_history_point["price_history_point_date"].strftime('%m/%d/%Y %H:%M:%S'),
            price_history_point["price_history_point_price"],
            price_history_point["price_history_point_volume"] * 2 # Hacky
            # price_history_point["price_history_point_rsi"]
        ])

    # Returning data

    return dumps({
        "price_history": data
    })

@main.route("/view_item_price_history_analysis")
def view_item_price_history_analysis():
    # Obtaining item details
    item_name = request.args.get("item_name")[1:]
    price_history = retrieve_item_price_history_analysis(item_name)

    # Returning data
    return {"price_history_analysis": price_history}
