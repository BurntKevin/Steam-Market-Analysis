"""
API for website
"""
# Server essentials
from json import dumps
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_caching import Cache

# Testing
from random import randint

# Database
from steam_database import SteamDatabase

# Flask Server
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
cache = Cache(application, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://steamscoutredis.xb4wpu.ng.0001.use1.cache.amazonaws.com:6379'})

# @application.route('/all_games')
# def all_game():
#     database = SteamDatabase(False)
#     results = database.query_database('SELECT name, icon FROM "Game"')
#     database.shutdown()

#     return dumps(results)

# @application.route('/all_items/<game>')
# def all_items_in_game(game):
#     database = SteamDatabase(False)
#     results = database.query_database(f"SELECT * FROM \"Item\" WHERE name='{game}'"")
#     database.shutdown()

#     return dumps(results)

# @application.route('/all_prices/<app_id>/<item>/<type>')
# def all_prices_for_item_in_game(app_id, item, type):
#     database = SteamDatabase(False)
#     results = database.query_database(f"SELECT market_hash_name, time, median_price, volume FROM \"{type}\" WHERE market_hash_name='{database.clean_market_hash_name(item)}'")
#     database.shutdown()

#     return dumps(results, default=str)

@application.route("/test")
def test():
    """
    Returns Hello World as a test to ensure server is still working
    """
    return "Hello World"

@application.route("/test_cache/<echo>")
@cache.cached(timeout=10)
def echo_back(echo):
    """
    Returns a string typed by the user as a test to ensure cache is working
    """
    return f"You Typed: {echo} {randint(3, 13300)}"

@application.route("/market_overview/")
@cache.cached(timeout=3600)
def market_overview():
    """
    Obtain's price and volume of the Steam Market
    """
    database = SteamDatabase(False)
    results = database.query_database("""
        SELECT daily_price_action.time as time, daily_price_action.volume as volume, daily_hour_price_action.high as high, daily_hour_price_action.low as low, daily_price_action.median_price as close
        FROM (SELECT time::date as time, sum(volume) as volume, sum(median_price) as median_price
            FROM "PriceDaily"
            GROUP BY time::date
            ORDER BY time) as daily_price_action
            LEFT JOIN
            (SELECT time::date as time, max(median_price) as high, min(median_price) as low
            FROM (SELECT time as time, sum(median_price) as median_price
                FROM "PriceHourly"
                GROUP BY time
                ORDER BY time) as hourly_price_action
            GROUP BY time::date
            ORDER BY time::date) as daily_hour_price_action
        ON daily_price_action.time=daily_hour_price_action.time
    """)
    database.shutdown()

    return dumps(results, default=str)

@application.route("/transaction_amount/")
@cache.cached(timeout=3600)
def transaction_amount():
    """
    Obtain's total volume price of the Steam Market
    """
    database = SteamDatabase(False)
    results = database.query_database("""
        SELECT time::date as time, sum(median_price * volume) as transaction_volume
        FROM "PriceDaily"
        GROUP BY time
    """)
    database.shutdown()

    return dumps(results, default=str)

if __name__ == "__main__":
    application.run()
