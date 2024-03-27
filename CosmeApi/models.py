from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    phases = db.relationship('Phase', backref='recipe', lazy=True, cascade="all, delete-orphan")
    instructions = db.Column(db.Text, nullable=True)
    version_of = db.Column(db.Integer, nullable=True)

class Ingredient(db.Model):
    CAS = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
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
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    note = db.Column(db.Text, nullable=True)
    order_number = db.Column(db.Integer, nullable=False)

class RecipeIngredientPhase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    phase_id = db.Column(db.Integer, db.ForeignKey('phase.id', ondelete="CASCADE"), nullable=False)
    CAS = db.Column(db.String(100), db.ForeignKey('ingredient.CAS', ondelete='RESTRICT'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    scent = db.Column(db.Float, nullable=False)
    stability = db.Column(db.Float, nullable=False)
    texture = db.Column(db.Float, nullable=False)
    efficacy = db.Column(db.Float, nullable=False)
    tolerance = db.Column(db.Float, nullable=False)

    # Relationship to Recipe
    recipe = db.relationship('Recipe', backref=db.backref('ratings', lazy=True))

    @property
    def average_rating(self):
        return (self.scent + self.stability + self.texture + self.efficacy + self.tolerance) / 5
