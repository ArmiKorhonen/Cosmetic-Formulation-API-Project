from db_setup import db, app  # Ensure db_setup.py correctly initializes db and app
from db_setup import Recipe, Phase, RecipeIngredientPhase, Ingredient

def fetch_and_print_recipes():
    with app.app_context():
        recipes = Recipe.query.all()  # Fetch all recipes from the database
        for recipe in recipes:
            print(f"Title: {recipe.title}, Description: {recipe.description}")
            print(f"Rating: {recipe.rating}, Instructions: {recipe.instructions}")
            
            # Fetch and print phases ordered by their order_number
            phases = Phase.query.filter_by(recipe_id=recipe.id).order_by(Phase.order_number).all()
            for phase in phases:
                print(f"  Phase: {phase.name}, Note: {phase.note}, Order: {phase.order_number}")
                
                # Fetch and print ingredients for the current phase
                ingredient_phases = RecipeIngredientPhase.query.filter_by(phase_id=phase.id).all()
                for ingredient_phase in ingredient_phases:
                    ingredient = Ingredient.query.get(ingredient_phase.ingredient_id)
                    if ingredient:  # Check if the ingredient exists
                        print(f"    Ingredient: {ingredient.name}, Quantity: {ingredient_phase.quantity}")
                        print(f"    INCI Name: {ingredient.INCI_name}, Function: {ingredient.function}")
                        print(f"    Description: {ingredient.description}")
                        print(f"    pH Min: {ingredient.ph_min}, pH Max: {ingredient.ph_max}, Temp Min: {ingredient.temp_min}, Temp Max: {ingredient.temp_max}")
                        print(f"    Use Level Min: {ingredient.use_level_min}, Use Level Max: {ingredient.use_level_max}\n")

if __name__ == '__main__':
    fetch_and_print_recipes()
