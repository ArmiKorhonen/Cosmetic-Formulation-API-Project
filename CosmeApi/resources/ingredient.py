from flask_restful import Resource, abort
from flask import request
from sqlalchemy.exc import IntegrityError
from CosmeApi.models import db, Ingredient

class IngredientCollection(Resource):
    """ Get the list of all of the ingredients in the collection"""
    def get(self):
        ingredients = Ingredient.query.all()
        ingredients_list = {
            '@controls': {
                'self': {'href': '/api/ingredients', 'method': 'GET'},
                'addIngredient': {
                    'href': '/api/ingredients',
                    'method': 'POST',
                    'encoding': 'application/json',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'CAS': {'type': 'string'},
                            'name': {'type': 'string'},
                            'INCI_name': {'type': 'string'},
                            'function': {'type': 'string'},
                            'description': {'type': 'string'},
                            'ph_min': {'type': 'number'},
                            'ph_max': {'type': 'number'},
                            'temp_min': {'type': 'number'},
                            'temp_max': {'type': 'number'},
                            'use_level_min': {'type': 'number'},
                            'use_level_max': {'type': 'number'},
                        }
                    }
                }
            },
            'items': [{
                'name': ingredient.name,
                'INCI_name': ingredient.INCI_name,
                'CAS': ingredient.CAS,
                'function': ingredient.function,
                'description': ingredient.description,
                'ph_min': ingredient.ph_min,
                'ph_max': ingredient.ph_max,
                'temp_min': ingredient.temp_min,
                'temp_max': ingredient.temp_max,
                'use_level_min': ingredient.use_level_min,
                'use_level_max': ingredient.use_level_max,
                '@controls': {
                    'self': {'href': f'/api/ingredients/{ingredient.CAS}', 'method': 'GET'},
                    'edit': {'href': f'/api/ingredients/{ingredient.CAS}', 'method': 'PUT'},
                    'delete': {'href': f'/api/ingredients/{ingredient.CAS}', 'method': 'DELETE'}
                }
            } for ingredient in ingredients]}
        return ingredients_list

    # Add a new ingredient to the collection
    def post(self):
        data = request.get_json(force=True)

        # Validate required fields
        required_fields = ['CAS', 'name', 'INCI_name']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 400

        new_ingredient = Ingredient(
            name=data['name'],
            INCI_name=data['INCI_name'],
            CAS=data['CAS'],
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

        return {
            'name': new_ingredient.name,
            'INCI_name': new_ingredient.INCI_name,
            'CAS': new_ingredient.CAS,
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

    # Get one ingredient by CAS number
    def get(self, cas):
        ingredient = Ingredient.query.filter_by(CAS=cas).first_or_404()
        return {
            'name': ingredient.name,
            'INCI_name': ingredient.INCI_name,
            'CAS': ingredient.CAS,
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
    def put(self, cas):
        ingredient = Ingredient.query.filter_by(CAS=cas).first_or_404()
        data = request.get_json(force=True)
        
        ingredient.name = data.get('name', ingredient.name)
        ingredient.INCI_name = data.get('INCI_name', ingredient.INCI_name)
        ingredient.CAS = data.get('CAS', ingredient.CAS)
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
            'name': ingredient.name,
            'INCI_name': ingredient.INCI_name,
            'CAS': ingredient.CAS,
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
    def delete(self, cas):
        ingredient = Ingredient.query.filter_by(CAS=cas).first_or_404()
        db.session.delete(ingredient)
        db.session.commit()
        return '', 204