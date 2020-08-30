"""
Server functions
"""

# Standard Libraries
from flask import Blueprint, request
from flask import Flask
from flask_cors import CORS

# Custom Libraries
from scraper import get_items_price_history, get_item_details
from database import upload_game_data, retrieve_all_game_basic_data, retrieve_game_items_basic_data, retrieve_price_history_data
from models import db

# Setting up server
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)

# Setting up database
db.init_app(app)
db.create_all(app=app)

@app.route("/add_game", methods=["POST"])
def add_game():
    """
    Adds or updates a game to the latest information
    """
    # Obtaining request details
    game_data = request.get_json()

    # Getting game data to add
    game = get_items_price_history(game_data["gameId"])

    # Saving the game's details
    upload_game_data(db, game)

    return "Done", 201

@app.route("/add_item", methods=["POST"])
def add_item():
    """
    Adds or updates item(s) to the latest information
    All items which are found by the query will be added
    """
    # Obtaining request details
    item_data = request.get_json()

    # Getting game data to add
    games = get_item_details(item_data["itemName"])

    # Saving each item's details
    for game in games:
        upload_game_data(db, game)

    return "Done", 201

@app.route("/view_games")
def all_game_basic_data():
    """
    Obtains basic game data for the user
    """
    # Getting all games
    games = retrieve_all_game_basic_data()

    # Returning data
    return {"games": games}

@app.route("/view_game_items")
def game_items_basic_data():
    """
    Obtains basic item data for the user
    """
    # Obtaining item details
    game_id = request.args.get("game_id")[1:]
    items = retrieve_game_items_basic_data(game_id)

    # Returning data
    return {"items": items}

@app.route("/view_item_price_history")
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

@app.route("/view_item_price_history_chart")
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
            price_history_point.rsi,
            price_history_point.macd,
        ])

    # Returning data
    return {"price_history": data}

# Running
if __name__ == "__main__":
    app.run()
