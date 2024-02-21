from flask_restful import Resource, abort
from models import db, Ingredient
from flask import request
from sqlalchemy.exc import IntegrityError

class IngredientCollection(Resource):
    # Get the list of all of the ingredients in the collection
    def get(self):
        ingredients = Ingredient.query.all()
        ingredients_list = [{
            'id': ingredient.id,
            'name': ingredient.name,
            'INCI_name': ingredient.INCI_name,
            'function': ingredient.function,
            'description': ingredient.description,
            'ph_min': ingredient.ph_min,
            'ph_max': ingredient.ph_max,
            'temp_min': ingredient.temp_min,
            'temp_max': ingredient.temp_max,
            'use_level_min': ingredient.use_level_min,
            'use_level_max': ingredient.use_level_max
        } for ingredient in ingredients]
        return ingredients_list

    # Add a new ingredient to the collection
    def post(self):
        data = request.get_json(force=True)
        new_ingredient = Ingredient(
            name=data['name'],
            INCI_name=data['INCI_name'],
            function=data.get('function', ''),
            description=data.get('description', ''),
            ph_min=data.get('ph_min'),
            ph_max=data.get('ph_max'),
            temp_min=data.get('temp_min'),
            temp_max=data.get('temp_max'),
            use_level_min=data.get('use_level_min'),
            use_level_max=data.get('use_level_max')
        )
        db.session.add(new_ingredient)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Ingredient with the given name or INCI_name already exists.")
        # In your post method, instead of return new_ingredient.to_dict(), 201
        return {
            'id': new_ingredient.id,
            'name': new_ingredient.name,
            'INCI_name': new_ingredient.INCI_name,
            'function': new_ingredient.function,
            'description': new_ingredient.description,
            'ph_min': new_ingredient.ph_min,
            'ph_max': new_ingredient.ph_max,
            'temp_min': new_ingredient.temp_min,
            'temp_max': new_ingredient.temp_max,
            'use_level_min': new_ingredient.use_level_min,
            'use_level_max': new_ingredient.use_level_max
        }, 201


class IngredientItem(Resource):
    # Get one ingredient
    def get(self, id):
        ingredient = Ingredient.query.get_or_404(id)
        return {
            'id': ingredient.id,
            'name': ingredient.name,
            'INCI_name': ingredient.INCI_name,
            'function': ingredient.function,
            'description': ingredient.description,
            'ph_min': ingredient.ph_min,
            'ph_max': ingredient.ph_max,
            'temp_min': ingredient.temp_min,
            'temp_max': ingredient.temp_max,
            'use_level_min': ingredient.use_level_min,
            'use_level_max': ingredient.use_level_max
        }

    # Update the information of one existing ingredient
    def put(self, id):
        ingredient = Ingredient.query.get_or_404(id)
        data = request.get_json(force=True)
        
        ingredient.name = data.get('name', ingredient.name)
        ingredient.INCI_name = data.get('INCI_name', ingredient.INCI_name)
        ingredient.function = data.get('function', ingredient.function)
        ingredient.description = data.get('description', ingredient.description)
        ingredient.ph_min = data.get('ph_min', ingredient.ph_min)
        ingredient.ph_max = data.get('ph_max', ingredient.ph_max)
        ingredient.temp_min = data.get('temp_min', ingredient.temp_min)
        ingredient.temp_max = data.get('temp_max', ingredient.temp_max)
        ingredient.use_level_min = data.get('use_level_min', ingredient.use_level_min)
        ingredient.use_level_max = data.get('use_level_max', ingredient.use_level_max)
        
        db.session.commit()

        # Return the updated ingredient as a dictionary
        return {
            'id': ingredient.id,
            'name': ingredient.name,
            'INCI_name': ingredient.INCI_name,
            'function': ingredient.function,
            'description': ingredient.description,
            'ph_min': ingredient.ph_min,
            'ph_max': ingredient.ph_max,
            'temp_min': ingredient.temp_min,
            'temp_max': ingredient.temp_max,
            'use_level_min': ingredient.use_level_min,
            'use_level_max': ingredient.use_level_max
        }, 200

    # Delete one ingredient
    def delete(self, id):
        ingredient = Ingredient.query.get_or_404(id)
        db.session.delete(ingredient)
        db.session.commit()
        return '', 204