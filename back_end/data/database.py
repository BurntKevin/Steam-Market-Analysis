"""
Functions to allow access to the database easier
"""
from back_end.data.models import Game as db_game, Item as db_item, PriceHistoryPoint as db_pricehistorypoint
from back_end.scraper.scraper_data import Game as sc_game, Item as sc_item, PriceHistoryPoint as sc_pricehistorypoint

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
        game_detail = Game(game.game_id)
        game_data.append({
            "game": game_detail.game_id
            "game_icon": game_detail.game_icon()
        })

    # Returning game ids
    return game_ids
