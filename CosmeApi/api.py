from flask import Blueprint
from flask_restful import Api
from CosmeApi.resources.ingredient import IngredientCollection, IngredientItem
from CosmeApi.resources.recipe import RecipeCollection, RecipeItem

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Register resources
api.add_resource(IngredientCollection, '/ingredients')
api.add_resource(IngredientItem, '/ingredients/<int:id>')
api.add_resource(RecipeCollection, '/recipes') 
api.add_resource(RecipeItem, '/recipes/<int:id>')