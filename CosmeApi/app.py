"""
Flask application setup with CORS, Flask-Migrate, and a SQLite database.
This module initializes the app and its configurations.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from CosmeApi.models import db
from CosmeApi.api import api_bp  # Adjusted based on the app's structure to avoid import issues

class Config:
    """Configuration class storing database settings."""
    SQLALCHEMY_DATABASE_URI = "sqlite:///cosme-api-project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    flask_app = Flask(__name__)  # Rename variable to avoid shadowing outer scope

    # Enable CORS for all routes and origins
    CORS(flask_app)

    # Use the default configuration defined by the Config class
    flask_app.config.from_object(Config)

    # If a test configuration is passed, apply it to override the default config
    if test_config is not None:
        flask_app.config.update(test_config)

    db.init_app(flask_app)
    Migrate(flask_app, db)  # Initialize Flask-Migrate with the app and db

    flask_app.register_blueprint(api_bp)

    return flask_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
