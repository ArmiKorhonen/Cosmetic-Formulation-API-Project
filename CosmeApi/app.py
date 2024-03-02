from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from CosmeApi.models import db

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///cosme-api-project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # Use the default configuration defined by the Config class
    app.config.from_object(Config)
    
    # If a test configuration is passed, apply it to override the default config
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate with the app and db

    # Import and register the API blueprint after the app is configured
    from CosmeApi.api import api_bp  # Ensure api.py doesn't cause imports before db is ready
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
