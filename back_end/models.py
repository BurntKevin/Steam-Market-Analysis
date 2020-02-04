"""
Database data structure
"""

from flask_sqlalchemy import SQLAlchemy

# Obtaining database
db = SQLAlchemy()

class Game(db.Model):
    """
    Game details: name, game_id, items in game
    """
    # Game details
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)

    # References
    items = db.relationship("Item", backref="game", lazy=True)

class Item(db.Model):
    """
    Item details: name, icon, associated game id, price history of item
    """
    # Item details
    name = db.Column(db.String(50), primary_key=True)
    icon = db.Column(db.String(150), nullable=False)

    # References
    game_id = db.Column(db.Integer, db.ForeignKey("game.game_id"), nullable=False)
    price_history = db.relationship("PriceHistoryPoint", backref="Item", lazy=True)

class PriceHistoryPoint(db.Model):
    """
    Price history point details: date, price, volume, rsi, macd, associated
    item name
    """
    # PriceHistoryPoint details
    date = db.Column(db.DateTime, primary_key=True)
    price = db.Column(db.Float, nullable=True, primary_key=True)
    volume = db.Column(db.Integer, nullable=False, primary_key=True)
    rsi = db.Column(db.Float, nullable=True, primary_key=True)
    macd = db.Column(db.Float, nullable=True, primary_key=True)
    percentage_change = db.Column(db.Float, nullable=True, primary_key=True)
    turnover = db.Column(db.Float, nullable=True, primary_key=True)

    # References
    item_name = db.Column(db.String(50), db.ForeignKey("item.name"), nullable=False, primary_key=True)
