from flask_restful import Resource, abort
from CosmeApi.models import db, Rating, Recipe
from flask import request
from flask import jsonify

class RecipeRatingCollection(Resource):
    # Add a new rating to a recipe
    def post(self, recipe_id):
        data = request.get_json(force=True)
        
        # Check if the recipe exists
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            abort(404, message=f"Recipe with id {recipe_id} not found.")
        
        # Proceed with adding the new rating since the recipe exists
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
                'average_rating': new_rating.average_rating
            }, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Failed to add rating due to an error: {e}")

class RecipeRating(Resource):
    # Retrieve the average ratings for a specific recipe
    def get(self, recipe_id):
        ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
        if not ratings:
            return {'message': f"No ratings found for recipe with id {recipe_id}"}, 404
        
        # Calculate the average for each category and overall
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
            'averages': averages
        }, 200
