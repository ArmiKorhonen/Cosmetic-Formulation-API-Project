from flask_restful import Resource
from models import db, Ingredient
from flask import request

class IngredientCollection(Resource):
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
        return new_ingredient.to_dict(), 201

class IngredientItem(Resource):
    def get(self, id):
        ingredient = Ingredient.query.get_or_404(id)
        # Return the ingredient as a dictionary
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

    def put(self, id):
        ingredient = Ingredient.query.get_or_404(id)
        data = request.get_json(force=True)
        # Update ingredient attributes here based on data
        # Example: ingredient.name = data.get('name', ingredient.name)
        db.session.commit()
        # Return the updated ingredient as a dictionary
        return {
            'id': ingredient.id,
            'name': ingredient.name,
            # add the rest of the fields here as needed
        }

    def delete(self, id):
        ingredient = Ingredient.query.get_or_404(id)
        db.session.delete(ingredient)
        db.session.commit()
        return '', 204