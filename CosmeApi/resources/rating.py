"""
This module defines the RESTful resource classes for managing recipe
ratings within the CosmeApi project.
It provides endpoints for adding new ratings to recipes, retrieving individual ratings,
and calculating average ratings for recipes.
"""

from flask_restful import Resource, abort
from flask import request
from CosmeApi.models import db, Rating, Recipe

class RecipeRatingCollection(Resource):
    """
    Resource for managing and accessing collections of ratings for a specific recipe.
    """
    # Add a new rating to a recipe
    def post(self, recipe_id):
        """
        Adds a new rating to a specific recipe. Accepts JSON input containing the rating details.
        Validates the existence of the recipe and commits the new rating to the database.
        """
        data = request.get_json(force=True)

        # Check if the recipe exists
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            abort(404, message=f"Recipe with id {recipe_id} not found.")

        new_rating = Rating(
            recipe_id=recipe_id,
            scent=data['scent'],
            stability=data['stability'],
            texture=data['texture'],
            efficacy=data['efficacy'],
            tolerance=data['tolerance']
        )

        db.session.add(new_rating)
        try:
            db.session.commit()
            return {
                'id': new_rating.id,
                'recipe_id': new_rating.recipe_id,
                'scent': new_rating.scent,
                'stability': new_rating.stability,
                'texture': new_rating.texture,
                'efficacy': new_rating.efficacy,
                'tolerance': new_rating.tolerance,
                '@controls': {
                    'self': {
                        'href': f'/api/recipes/{recipe_id}/ratings/{new_rating.id}',
                        'method': 'GET'
                    }
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Failed to add rating due to an error: {str(e)}")

    def get(self, recipe_id):
        """
        Retrieves all ratings for a specific recipe and calculates
        average ratings across multiple categories.
        Returns the averages and individual ratings in a structured JSON response.
        """
        ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
        if not ratings:
            return {'message': f"No ratings found for recipe with id {recipe_id}"}, 404

        averages = {
            'scent': sum(r.scent for r in ratings) / len(ratings),
            'stability': sum(r.stability for r in ratings) / len(ratings),
            'texture': sum(r.texture for r in ratings) / len(ratings),
            'efficacy': sum(r.efficacy for r in ratings) / len(ratings),
            'tolerance': sum(r.tolerance for r in ratings) / len(ratings),
        }
        averages['overall'] = sum(averages.values()) / len(averages)

        return {
            'recipe_id': recipe_id,
            'averages': averages,
            '@controls': {
                'self': {
                    'href': f'/api/recipes/{recipe_id}/ratings',
                    'method': 'GET'
                }
            }
        }, 200

class RecipeRating(Resource):
    """
    Resource for retrieving average ratings of a specific recipe.
    """
    # Retrieve the average ratings for a specific recipe
    def get(self, recipe_id):
        """
        Calculates and returns the average ratings for a specific
        recipe based on multiple rating criteria.
        Provides a detailed view of rating averages in JSON format
        with hypermedia controls for API navigation.
        """
        ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
        if not ratings:
            return {'message': f"No ratings found for recipe with id {recipe_id}"}, 404

        averages = {
            'scent': sum(r.scent for r in ratings) / len(ratings),
            'stability': sum(r.stability for r in ratings) / len(ratings),
            'texture': sum(r.texture for r in ratings) / len(ratings),
            'efficacy': sum(r.efficacy for r in ratings) / len(ratings),
            'tolerance': sum(r.tolerance for r in ratings) / len(ratings),
        }
        averages['overall'] = sum(averages.values()) / len(averages)

        return {
            'recipe_id': recipe_id,
            'averages': averages,
            '@controls': {
                'self': {
                    'href': f'/api/recipes/{recipe_id}/ratings/average',
                    'method': 'GET'
                }
            }
        }, 200
