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

@application.route('/all_games')
def all_game():
    database = SteamDatabase(False)
    results = database.query_database('SELECT name, icon FROM "Game"')
    database.shutdown()

    return dumps(results)

@application.route('/all_items/<game>')
def all_items_in_game(game):
    database = SteamDatabase(False)
    results = database.query_database(f"SELECT * FROM \"Item\" WHERE name='{game}'")
    database.shutdown()

    return dumps(results)

@application.route('/all_prices/<app_id>/<item>/<type>')
def all_prices_for_item_in_game(app_id, item, type):
    database = SteamDatabase(False)
    results = database.query_database(f"SELECT market_hash_name, time, median_price, volume FROM \"{type}\" WHERE market_hash_name='{database.clean_market_hash_name(item)}'")
    database.shutdown()

    return dumps(results, default=str)

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

@application.route("/market_overview")
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

@application.route("/transaction_amount")
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

@application.route("/market_seasonality")
@cached.cached(timeout=3600)
def market_seasonality():
    """
    Seasonality of the entire market calculated using the earliest date of a
    month and the latest date of a month:
    (end_price - start_price) / start_price
    """
    database = SteamDatabase(False)
    results = database.query_database("""
        SELECT start_month_prices.month, AVG(((end_month_prices.median_price - start_month_prices.median_price) / start_month_prices.median_price) * 100) as seasonal_percentage_move
        FROM (SELECT daily_price_action.month, daily_price_action.year, daily_price_action.median_price, daily_price_action.market_hash_name
            FROM (SELECT max(day) as day, month, year, market_hash_name
                FROM
                (SELECT date_part('day', time) as day, date_part('month', time) as month, date_part('year', time) as year, market_hash_name
                FROM "PriceDaily") as split_data
                GROUP BY month, year, market_hash_name) as end_month_data
                JOIN
                (SELECT date_part('day', time) as day, date_part('month', time) as month, date_part('year', time) as year, market_hash_name, median_price
                FROM "PriceDaily") as daily_price_action
                ON daily_price_action.market_hash_name = end_month_data.market_hash_name
                AND daily_price_action.day = end_month_data.day
                AND daily_price_action.month = end_month_data.month
                AND daily_price_action.year = end_month_data.year
            GROUP BY daily_price_action.month, daily_price_action.year, daily_price_action.median_price, daily_price_action.market_hash_name) as end_month_prices
            JOIN
            (SELECT daily_price_action.month, daily_price_action.year, daily_price_action.median_price, daily_price_action.market_hash_name
            FROM (SELECT min(day) as day, month, year, market_hash_name
                FROM
                (SELECT date_part('day', time) as day, date_part('month', time) as month, date_part('year', time) as year, market_hash_name
                FROM "PriceDaily") as split_data
                GROUP BY month, year, market_hash_name) as start_month_data
                JOIN
                (SELECT date_part('day', time) as day, date_part('month', time) as month, date_part('year', time) as year, market_hash_name, median_price
                FROM "PriceDaily") as daily_price_action
                ON daily_price_action.market_hash_name = start_month_data.market_hash_name
                AND daily_price_action.day = start_month_data.day
                AND daily_price_action.month = start_month_data.month
                AND daily_price_action.year = start_month_data.year
            GROUP BY daily_price_action.month, daily_price_action.year, daily_price_action.median_price, daily_price_action.market_hash_name) as start_month_prices
            ON start_month_prices.month = end_month_prices.month
            AND start_month_prices.year = end_month_prices.year
            AND start_month_prices.market_hash_name = end_month_prices.market_hash_name
        GROUP BY start_month_prices.month
    """)

    return dumps(results, default=str)

if __name__ == "__main__":
    application.run()
