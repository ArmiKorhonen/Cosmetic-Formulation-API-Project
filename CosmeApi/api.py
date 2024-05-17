"""
This module sets up the API routes for the CosmeApi application, including endpoints.
"""

from flask import Blueprint
from flask_restful import Api
from CosmeApi.resources.ingredient import IngredientCollection, IngredientItem
from CosmeApi.resources.recipe import RecipeCollection, RecipeItem
from CosmeApi.resources.rating import RecipeRatingCollection, RecipeRating

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Register resources
api.add_resource(IngredientCollection, '/ingredients')
api.add_resource(IngredientItem, '/ingredients/<string:cas>')
api.add_resource(RecipeCollection, '/recipes')
api.add_resource(RecipeItem, '/recipes/<int:id>')
api.add_resource(RecipeRatingCollection, '/recipes/<int:recipe_id>/ratings')
api.add_resource(RecipeRating, '/recipes/<int:recipe_id>/ratings/<int:rating_id>')
