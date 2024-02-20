from flask import Blueprint
from flask_restful import Api
from resources.ingredient import IngredientCollection, IngredientItem

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Register resources
api.add_resource(IngredientCollection, '/ingredients')
api.add_resource(IngredientItem, '/ingredients/<int:id>')
