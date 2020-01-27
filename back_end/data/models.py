from back_end.__init__ import db
from datetime import datetime

class Game(db.Model):
    # Game details
    game_id = db.Column(db.Integer, primary_key=True)

    # References
    items = db.relationship("Item", backref="game", lazy=True)

class Item(db.Model):
    # Item details
    name = db.Column(db.String(50), primary_key=True)
    icon = db.Column(db.String(150), nullable=False)

    # References
    game_id = db.Column(db.Integer, db.ForeignKey("game.game_id"), nullable=False)
    price_history = db.relationship("PriceHistoryPoint", backref="Item", lazy=True)

class PriceHistoryPoint(db.Model):
    # PriceHistoryPoint details
    date = db.Column(db.DateTime, primary_key=True)
    price = db.Column(db.Float, nullable=False, primary_key=True)
    volume = db.Column(db.Integer, nullable=False, primary_key=True)

    # References
    item_name = db.Column(db.String(50), db.ForeignKey("item.name"), nullable=False, primary_key=True)
