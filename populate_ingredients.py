import json
from db_setup import db, app 
from db_setup import Ingredient

def load_ingredients_from_json(json_filepath='ingredients.json'):
    with app.app_context():
        with open(json_filepath, 'r') as file:
            ingredients_data = json.load(file)
            for data in ingredients_data:
                ingredient = Ingredient(
                    name=data['name'],
                    INCI_name=data['INCI_name'],
                    function=data['function'],
                    description=data['description'],
                    ph_min=data.get('ph_min'),
                    ph_max=data.get('ph_max'),
                    temp_min=data.get('temp_min'),
                    temp_max=data.get('temp_max'),
                    use_level_min=data['use_level_min'],
                    use_level_max=data['use_level_max']
                )
                db.session.add(ingredient)
            db.session.commit()

if __name__ == '__main__':
    load_ingredients_from_json()
