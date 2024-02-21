from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phases = db.relationship('Phase', backref='recipe', lazy=True)
    rating = db.Column(db.Integer, nullable=True)
    instructions = db.Column(db.Text, nullable=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    INCI_name = db.Column(db.String(100), nullable=False)
    function = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    ph_min = db.Column(db.Float, nullable=True)
    ph_max = db.Column(db.Float, nullable=True)
    temp_min = db.Column(db.Float, nullable=True)
    temp_max = db.Column(db.Float, nullable=True)
    use_level_min = db.Column(db.Float, nullable=True)
    use_level_max = db.Column(db.Float, nullable=True)

class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    note = db.Column(db.Text, nullable=True)

class RecipeIngredientPhase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    phase_id = db.Column(db.Integer, db.ForeignKey('phase.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

class RecipeVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipe = db.relationship('Recipe', backref=db.backref('versions', lazy=True))
