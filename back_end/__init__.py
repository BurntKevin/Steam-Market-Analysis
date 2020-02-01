"""
Initialise flask server
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

def create_app():
    """
    Creates flask app
    """
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    DB.init_app(app)

    from .server import MAIN
    app.register_blueprint(MAIN)

    return app
