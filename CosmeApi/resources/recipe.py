from flask_restful import Resource, abort
from flask import request, jsonify
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from CosmeApi.models import db, Recipe, Phase, Ingredient, RecipeIngredientPhase

class RecipeCollection(Resource):
    def get(self):
        recipes = Recipe.query.all()
        recipes_list = {
            '@controls': {
                'self': {'href': '/api/recipes', 'method': 'GET'},
                'addRecipe': {
                    'href': '/api/recipes',
                    'method': 'POST',
                    'encoding': 'application/json',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'title': {'type': 'string'},
                            'description': {'type': 'string', 'optional': True},
                            'instructions': {'type': 'string', 'optional': True},
                            'version_of': {'type': 'integer', 'optional': True},
                            'phases': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string'},
                                        'note': {'type': 'string', 'optional': True},
                                        'ingredients': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'cas': {'type': 'string'},
                                                    'quantity': {'type': 'number'}
                                                }
                                            }
                                        }
                                    },
                                    'required': ['name']
                                }
                            }
                        },
                        'required': ['title']
                    }
                }
            },
            'items': []
        }
        for recipe in recipes:
            recipe_data = {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'instructions': recipe.instructions,
                'version_of': recipe.version_of,
                'phases': []
            }
            sorted_phases = sorted(recipe.phases, key=lambda phase: phase.order_number)
            for phase in sorted_phases:
                phase_data = {
                    'name': phase.name,
                    'note': phase.note,
                    'order_number': phase.order_number,
                    'ingredients': []
                }
                ingredient_phases = RecipeIngredientPhase.query.filter_by(phase_id=phase.id).all()
                for ingredient_phase in ingredient_phases:
                    ingredient = Ingredient.query.get(ingredient_phase.CAS)
                    if ingredient:
                        phase_data['ingredients'].append({
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
                            'quantity': ingredient_phase.quantity
                        })
                recipe_data['phases'].append(phase_data)
            recipes_list['items'].append(recipe_data)
        return jsonify(recipes_list)

    def post(self):
        data = request.get_json(force=True)
        new_recipe = Recipe(
            title=data['title'],
            description=data.get('description', ''),
            instructions=data.get('instructions', ''),
            version_of=data.get('version_of', None)
        )
        db.session.add(new_recipe)
        try:
            db.session.flush()  # Assign an ID to new_recipe without committing the transaction
            for index, phase_data in enumerate(data['phases']):
                phase = Phase(
                    name=phase_data['name'],
                    note=phase_data.get('note', ''),
                    recipe_id=new_recipe.id,
                    order_number=index + 1
                )
                db.session.add(phase)
                db.session.flush()  # Assign an ID to phase for linking with ingredients
                for ingredient_data in phase_data['ingredients']:
                    recipe_ingredient_phase = RecipeIngredientPhase(
                        recipe_id=new_recipe.id,
                        phase_id=phase.id,
                        cas=ingredient_data['cas'],
                        quantity=ingredient_data['quantity']
                    )
                    db.session.add(recipe_ingredient_phase)
            db.session.commit()
            return {'message': 'Recipe created successfully', 'id': new_recipe.id}, 201
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while creating the recipe. {str(e)}")

class RecipeItem(Resource):
    def get(self, id):
        recipe = Recipe.query.get(id)
        if not recipe:
            abort(404, message=f"Recipe with id {id} not found.")
        recipe_data = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'instructions': recipe.instructions,
            'version_of': recipe.version_of,
            'phases': [],
            '@controls': {
                'self': {
                    'href': f'/api/recipes/{recipe.id}',
                    'method': 'GET'
                },
                'edit': {
                    'href': f'/api/recipes/{recipe.id}',
                    'method': 'PUT',
                    'encoding': 'application/json',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'title': {'type': 'string'},
                            'description': {'type': 'string', 'optional': True},
                            'instructions': {'type': 'string', 'optional': True},
                            'version_of': {'type': 'integer', 'optional': True},
                            'phases': {'type': 'array'}  # Define phase schema similarly
                        }
                    }
                },
                'delete': {
                    'href': f'/api/recipes/{recipe.id}',
                    'method': 'DELETE'
                }
            }
        }
        for phase in sorted(recipe.phases, key=lambda phase: phase.order_number):
            phase_data = {
                'name': phase.name,
                'note': phase.note,
                'order_number': phase.order_number,
                'ingredients': []
            }
            ingredient_phases = RecipeIngredientPhase.query.filter_by(phase_id=phase.id).all()
            for ingredient_phase in ingredient_phases:
                ingredient = Ingredient.query.get(ingredient_phase.CAS)
                if ingredient:
                    phase_data['ingredients'].append({
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
                        'quantity': ingredient_phase.quantity
                    })
            recipe_data['phases'].append(phase_data)
        return jsonify(recipe_data)

    def delete(self, id):
        recipe = Recipe.query.get(id)
        if not recipe:
            abort(404, message=f"Recipe with id {id} not found.")
        try:
            db.session.delete(recipe)
            db.session.commit()
            return {'message': f'Recipe with id {id} successfully deleted.'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to delete recipe. Error: {str(e)}")
