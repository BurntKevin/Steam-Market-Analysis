# Standard Libraries
from flask import Blueprint, jsonify, request

# Custom Libraries
from back_end.__init__ import db, create_app
from back_end.data.models import Game, Item, PriceHistoryPoint
from back_end.scraper.scraper import get_items_price_history
from back_end.data.database import upload_game_data, retrieve_game_data

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

@main.route("/games")
def games():
    # Getting requested game
    game_id = request.args.get("id")

    # Obtaining games
    games = retrieve_game_data(game_id)

    # Returning data
    return jsonify({
        "games": games.deobject()
    })
