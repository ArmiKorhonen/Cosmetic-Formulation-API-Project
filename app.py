from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///cosme-api-project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Assuming db is defined in models.py like so:
# db = SQLAlchemy()
from models import db  # Make sure this is correctly pointing to your models.py

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate with the app and db

    # Now that db is initialized, import and register your blueprint
    from api import api_bp  # Ensure api.py doesn't cause imports before db is ready
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
