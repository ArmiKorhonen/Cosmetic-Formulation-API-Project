from db_setup import db, app
from db_setup import Ingredient

def fetch_and_print_ingredients():
    with app.app_context():
        ingredients = Ingredient.query.all()  # Fetch all ingredients from the database
        for ingredient in ingredients:
            print(f"Name: {ingredient.name}, INCI Name: {ingredient.INCI_name}, Function: {ingredient.function}")
            print(f"Description: {ingredient.description}")
            print(f"pH Min: {ingredient.ph_min}, pH Max: {ingredient.ph_max}, Temp Min: {ingredient.temp_min}, Temp Max: {ingredient.temp_max}")
            print(f"Use Level Min: {ingredient.use_level_min}, Use Level Max: {ingredient.use_level_max}\n")

if __name__ == '__main__':
    fetch_and_print_ingredients()


