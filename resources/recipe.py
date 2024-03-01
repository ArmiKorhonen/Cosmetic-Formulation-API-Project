from flask_restful import Resource, abort
from models import db, Recipe, Phase, Ingredient, RecipeIngredientPhase
from flask import request
from datetime import datetime
from flask import jsonify

class RecipeCollection(Resource):
    def get(self):
        recipes = Recipe.query.all()
        recipes_list = []
        for recipe in recipes:
            # Serialize each recipe
            recipe_data = {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'rating': recipe.rating,
                'instructions': recipe.instructions,
                'version_of': recipe.version_of,
                'phases': []
            }

            # Sort the phases by order_number before iterating
            sorted_phases = sorted(recipe.phases, key=lambda phase: phase.order_number)

            # Include phases and their respective ingredients
            for phase in sorted_phases:
                phase_data = {
                    'name': phase.name,
                    'note': phase.note,
                    'order_number': phase.order_number,
                    'ingredients': []
                }

                # Query ingredients associated with the current phase
                ingredient_phases = RecipeIngredientPhase.query.filter_by(phase_id=phase.id).all()
                for ingredient_phase in ingredient_phases:
                    ingredient = Ingredient.query.get(ingredient_phase.ingredient_id)
                    if ingredient:  # Check if ingredient exists
                        phase_data['ingredients'].append({
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
                            'use_level_max': ingredient.use_level_max,
                            'quantity': ingredient_phase.quantity
                        })

                recipe_data['phases'].append(phase_data)

            recipes_list.append(recipe_data)

        return recipes_list
    
    def post(self):
        data = request.get_json(force=True)
        
        # Create the Recipe instance
        new_recipe = Recipe(
            title=data['title'],
            description=data.get('description', ''),
            rating=data.get('rating'),
            instructions=data.get('instructions', ''),
            version_of=data.get('version_of')
        )
        db.session.add(new_recipe)
        
        try:
            db.session.flush()  # Assign an ID to new_recipe without committing the transaction
            
            # Handle phases
            for index, phase_data in enumerate(data['phases']):  # Use enumerate to get the index (order)
                phase = Phase(
                    name=phase_data['name'],
                    note=phase_data['note'],
                    recipe_id=new_recipe.id,  # Link to the newly created recipe
                    order_number=index + 1  # Use index+1 as the order number (assuming order starts at 1)
                )
                db.session.add(phase)
                db.session.flush()  # Assign an ID to phase for linking with ingredients
                
                # Handle ingredients within each phase
                for ingredient_data in phase_data['ingredients']:
                    recipe_ingredient_phase = RecipeIngredientPhase(
                        recipe_id=new_recipe.id,
                        phase_id=phase.id,
                        ingredient_id=ingredient_data['ingredient_id'],
                        quantity=ingredient_data['quantity']
                    )
                    db.session.add(recipe_ingredient_phase)
            
            db.session.commit()  # Commit everything once all insertions are done
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while creating the recipe. {str(e)}")
        
        return {'message': 'Recipe created successfully', 'id': new_recipe.id}, 201

class RecipeItem(Resource):
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