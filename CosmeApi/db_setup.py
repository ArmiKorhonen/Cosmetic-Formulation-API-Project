"""
This module sets up the database for the CosmeApi application.
It configures the Flask app to connect to a SQLite database, initializes the SQLAlchemy ORM, 
and creates all necessary tables defined within the application models.
"""

from flask import Flask
from CosmeApi.models import db  # Adjust import according to your package structure

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cosme-api-project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the SQLAlchemy db object to your Flask app
db.init_app(app)

# Create a context for the application
with app.app_context():
    # Create all tables
    db.create_all()
