"""
Database data structure
"""

# Obtaining database
from back_end.__init__ import DB

class Game(DB.Model):
    """
    Game details: name, game_id, items in game
    """
    # Game details
    game_id = DB.Column(DB.Integer, primary_key=True)
    game_name = DB.Column(DB.String(50), nullable=False)

    # References
    items = DB.relationship("Item", backref="game", lazy=True)

class Item(DB.Model):
    """
    Item details: name, icon, associated game id, price history of item
    """
    # Item details
    name = DB.Column(DB.String(50), primary_key=True)
    icon = DB.Column(DB.String(150), nullable=False)

    # References
    game_id = DB.Column(DB.Integer, DB.ForeignKey("game.game_id"), nullable=False)
    price_history = DB.relationship("PriceHistoryPoint", backref="Item", lazy=True)

class PriceHistoryPoint(DB.Model):
    """
    Price history point details: date, price, volume, rsi, macd, associated
    item name
    """
    # PriceHistoryPoint details
    date = DB.Column(DB.DateTime, primary_key=True)
    price = DB.Column(DB.Float, nullable=True, primary_key=True)
    volume = DB.Column(DB.Integer, nullable=False, primary_key=True)
    rsi = DB.Column(DB.Float, nullable=True, primary_key=True)
    macd = DB.Column(DB.Float, nullable=True, primary_key=True)
    percentage_change = DB.Column(DB.Float, nullable=True, primary_key=True)
    turnover = DB.Column(DB.Float, nullable=True, primary_key=True)

    # References
    item_name = DB.Column(DB.String(50), DB.ForeignKey("item.name"), nullable=False, primary_key=True)
