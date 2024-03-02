# db_setup.py
from flask import Flask
from models import db, Recipe, Ingredient, Phase, RecipeIngredientPhase

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cosme-api-project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the SQLAlchemy db object to your Flask app
db.init_app(app)

# Create a context for the application
with app.app_context():
    # Create all tables
    db.create_all()
