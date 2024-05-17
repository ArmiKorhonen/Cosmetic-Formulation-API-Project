"""
Populate the database if empty.
"""

import json
from CosmeApi.app import db, create_app
from CosmeApi.models import Ingredient, Recipe, Phase, RecipeIngredientPhase

def clear_database():
    """Clear database"""
    # This will delete all data from the tables, resetting them
    db.session.query(RecipeIngredientPhase).delete()
    db.session.query(Phase).delete()
    db.session.query(Recipe).delete()
    db.session.query(Ingredient).delete()
    db.session.commit()

def load_data_from_json(json_filepath='../tests/database_data.json'):
    """Get all the data information from a json-file"""
    app = create_app()
    with app.app_context():
        with open(json_filepath, 'r') as file:
            data = json.load(file)

            # Load ingredients
            # Load ingredients
            for ingredient_data in data["ingredients"]:
                existing_ingredient = Ingredient.query.filter_by(CAS=ingredient_data["CAS"]).first()
                if not existing_ingredient:
                    ingredient = Ingredient(
                        CAS=ingredient_data["CAS"],
                        name=ingredient_data["name"],
                        INCI_name=ingredient_data["INCI_name"],
                        function=ingredient_data.get("function", None),
                        description=ingredient_data.get("description", None),
                        ph_min=ingredient_data.get("ph_min", None),
                        ph_max=ingredient_data.get("ph_max", None),
                        temp_min=ingredient_data.get("temp_min", None),
                        temp_max=ingredient_data.get("temp_max", None),
                        use_level_min=ingredient_data.get("use_level_min", None),
                        use_level_max=ingredient_data.get("use_level_max", None)
                    )
                    db.session.add(ingredient)
            db.session.commit()

            # Load recipes
            for recipe_data in data["recipes"]:
                recipe = Recipe(
                    title=recipe_data["title"],
                    description=recipe_data.get("description", ""),
                    rating=recipe_data.get("rating", None),
                    instructions=recipe_data.get("instructions", ""),
                    version_of=recipe_data.get("version_of", None)
                )
                db.session.add(recipe)
                db.session.flush()  # Flush to ensure the recipe ID is generated for use in phases

                # Load phases and their ingredients for each recipe
                for phase_data in recipe_data["phases"]:
                    phase = Phase(
                        name=phase_data["name"],
                        note=phase_data.get("note", ""),
                        order_number=phase_data["order_number"],
                        recipe_id=recipe.id
                    )
                    db.session.add(phase)
                    db.session.flush()

                    # Load ingredients for each phase
                    for ingredient_data in phase_data["ingredients"]:
                        ingredient = Ingredient.query.filter_by(CAS=ingredient_data["CAS"]).first()
                        if ingredient:
                            recipe_ingredient_phase = RecipeIngredientPhase(
                                recipe_id=recipe.id,
                                phase_id=phase.id,
                                CAS=ingredient_data['CAS'],
                                quantity=ingredient_data["quantity"]
                            )
                            db.session.add(recipe_ingredient_phase)

            db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        clear_database()
        load_data_from_json()
