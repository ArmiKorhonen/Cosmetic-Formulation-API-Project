import pytest
import os
import tempfile
import json
from CosmeApi.app import create_app, db
from CosmeApi.models import db, Ingredient, Recipe, Phase, RecipeIngredientPhase, Rating

def _populate_db(initial_data):
    # Load ingredients
    for ingredient_data in initial_data["ingredients"]:
        ingredient = Ingredient(**ingredient_data)
        db.session.add(ingredient)
    db.session.commit()  # Commit ingredients before adding recipes

    # Load recipes and possibly ratings
    for recipe_data in initial_data["recipes"]:
        recipe = Recipe(
            title=recipe_data["title"],
            description=recipe_data.get("description", ""),
            instructions=recipe_data.get("instructions", ""),
            version_of=recipe_data.get("version_of", None)
        )
        db.session.add(recipe)
        db.session.flush()  # Flush to assign IDs before adding phases and ratings

        # Assuming ratings data is part of recipe_data, which you might need to add
        if "ratings" in recipe_data:
            for rating_data in recipe_data["ratings"]:
                rating = Rating(
                    recipe_id=recipe.id,
                    scent=rating_data['scent'],
                    stability=rating_data['stability'],
                    texture=rating_data['texture'],
                    efficacy=rating_data['efficacy'],
                    tolerance=rating_data['tolerance']
                )
                db.session.add(rating)

        # Load phases if any
        for phase_index, phase_data in enumerate(recipe_data.get("phases", []), start=1):
            phase = Phase(
                name=phase_data["name"],
                note=phase_data.get("note", ""),
                order_number=phase_index,
                recipe_id=recipe.id
            )
            db.session.add(phase)
            db.session.flush()  # Flush to assign IDs before adding ingredients

            # Load ingredients for each phase
            for ingredient_phase_data in phase_data["ingredients"]:
                ingredient = Ingredient.query.filter_by(CAS=ingredient_phase_data["CAS"]).first()
                if ingredient:
                    recipe_ingredient_phase = RecipeIngredientPhase(
                        recipe_id=recipe.id,
                        phase_id=phase.id,
                        CAS=ingredient_phase_data["CAS"],
                        quantity=ingredient_phase_data["quantity"]
                    )
                    db.session.add(recipe_ingredient_phase)

    db.session.commit()  # Final commit to save everything


@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True,
    }
    
    app = create_app(config)
    
    # Construct the path to the JSON file
    current_dir = os.path.dirname(__file__)  # Get the directory where the test file is located
    json_file_path = os.path.join(current_dir, 'database_data.json')  # Adjust the path to your JSON file
    
    # Load the initial data from the JSON file
    with open(json_file_path, 'r') as json_file:
        initial_data = json.load(json_file)
    
    with app.app_context():
        db.create_all()
        _populate_db(initial_data)  # Populate the database using the loaded data
        print("All recipes in DB:", Recipe.query.all())
        print("All ratings in DB:", Rating.query.all())
        
    yield app.test_client()  # Use the test client for testing

    with app.app_context():
            db.session.remove()
            db.drop_all()

    os.close(db_fd)
    try:
        os.unlink(db_fname)  # Attempt to delete the temp file
    except PermissionError:
        print(f"Warning: Could not delete temporary database file at {db_fname}. File may be locked.")

            
def test_get_ingredients(client):
    """Test fetching all ingredients. Ensures ingredients are returned and checks basic structure."""
    response = client.get('/api/ingredients')
    assert response.status_code == 200
    assert isinstance(response.json, dict)  # Assuming your ingredients are returned as a dictionary with list inside
    assert 'items' in response.json  # Ensure that 'items' key exists
    assert len(response.json['items']) > 0  # Ensure that there's at least one ingredient

def test_add_ingredient(client):
    """Test adding a new ingredient."""
    new_ingredient = {
        'name': 'Test Ingredient',
        'INCI_name': 'Testus ingredientus',
        'CAS': 'xxx-xx-x',
        'function': 'Testing',
        'description': 'Used for testing purposes',
        'ph_min': 1,
        'ph_max': 14,
        'temp_min': 0,
        'temp_max': 100,
        'use_level_min': 0.1,
        'use_level_max': 10
    }
    response = client.post('/api/ingredients', json=new_ingredient)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == new_ingredient['name']

def test_add_ingredient_with_missing_fields(client):
    """Test adding an ingredient with missing required fields."""
    incomplete_ingredient = {
        'name': 'Incomplete Ingredient',
        'INCI_name': 'Testus ingredientus',
        'CAS': '',
        'function': 'Testing',
        'description': 'Used for testing purposes',
        'ph_min': 1,
        'ph_max': 14,
        'temp_min': 0,
        'temp_max': 100,
        'use_level_min': 0.1,
        'use_level_max': 10
    }
    response = client.post('/api/ingredients', json=incomplete_ingredient)
    assert response.status_code == 400  # Assuming 400 for bad request

def test_add_existing_ingredient(client):
    """Test adding an ingredient that already exists."""
    existing_ingredient = {
        "name": "Stearic Acid",
        "INCI_name": "Stearic Acid",
        "CAS": "57-11-4",
        "function": "Surfactant, Emulsifier",
        "description": "Stearic Acid is a fatty acid used as an emulsifier and surfactant. It has cleansing and emulsifying properties, making it useful in soaps and lotions.",
        "ph_min": 5.5,
        "ph_max": 8.0,
        "temp_min": 54.0,
        "temp_max": 70.0,
        "use_level_min": 0.5,
        "use_level_max": 5.0
    }
    response = client.post('/api/ingredients', json=existing_ingredient)
    assert response.status_code == 409  # Assuming 409 for conflict

def test_get_single_ingredient(client):
    """Test fetching a single ingredient by CAS number."""
    # Ensure a known ingredient exists; you might need to insert it during setup if necessary
    known_cas = '57-11-4'  # Example CAS number; adjust as necessary
    response = client.get(f'/api/ingredients/{known_cas}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['CAS'] == known_cas

def test_get_nonexistent_ingredient(client):
    """Test fetching a non-existent ingredient."""
    response = client.get('/api/ingredients/9999')  # Assuming this ID does not exist
    assert response.status_code == 404

def test_update_ingredient(client):
    """Test updating an ingredient."""
    known_cas = '57-11-4'  # Adjust based on a known CAS that exists in your test setup
    update_data = {'name': 'Updated Name'}
    response = client.put(f'/api/ingredients/{known_cas}', json=update_data)
    assert response.status_code == 200
    updated_data = response.get_json()
    assert updated_data['name'] == update_data['name']

def test_update_nonexistent_ingredient(client):
    """Test updating a non-existent ingredient."""
    response = client.put('/api/ingredients/9999', json={'name': 'Ghost Ingredient'})
    assert response.status_code == 404

def test_delete_ingredient(client):
    """Test deleting an ingredient."""
    # Ensure there's an ingredient to delete; you might need to insert it first during setup
    known_cas = '57-11-4'  # Adjust based on a known CAS that exists in your test setup
    response = client.delete(f'/api/ingredients/{known_cas}')
    assert response.status_code == 204

def test_delete_nonexistent_ingredient(client):
    """Test deleting a non-existent ingredient."""
    response = client.delete('/api/ingredients/9999')
    assert response.status_code == 404

def test_get_single_recipe(client):
    """Test fetching a single recipe by ID."""
    # Ensure a recipe exists; you might need to insert one if necessary
    response = client.get('/api/recipes/1')  # Adjust ID as necessary
    assert response.status_code == 200

def test_get_nonexistent_recipe(client):
    """Test fetching a non-existent recipe."""
    response = client.get('/api/recipes/9999')
    assert response.status_code == 404

def test_delete_recipe(client):
    """Test deleting a recipe."""
    # Ensure there's a recipe to delete; you might need to insert one first
    response = client.delete('/api/recipes/1')  # Adjust ID as necessary

def test_add_rating_to_recipe(client):
    """Test adding a new rating to an existing recipe."""
    recipe_id = 1  # Ensure this recipe ID exists in your test setup
    new_rating = {
        'scent': 5,
        'stability': 4,
        'texture': 5,
        'efficacy': 4,
        'tolerance': 5
    }
    response = client.post(f'/api/recipes/{recipe_id}/ratings', json=new_rating)
    assert response.status_code == 201
    data = response.get_json()
    assert data['recipe_id'] == recipe_id
    assert data['scent'] == new_rating['scent']

def test_add_rating_to_nonexistent_recipe(client):
    """Test adding a rating to a recipe that does not exist."""
    non_existent_recipe_id = 9999
    rating_data = {
        'scent': 5,
        'stability': 4,
        'texture': 5,
        'efficacy': 4,
        'tolerance': 5
    }
    response = client.post(f'/api/recipes/{non_existent_recipe_id}/ratings', json=rating_data)
    assert response.status_code == 404
    assert 'not found' in response.get_json()['message']

def test_get_average_ratings(client):
    """Test retrieving average ratings for a specific recipe."""
    recipe_id = 1  # Ensure this recipe ID exists and has ratings
    # Verify the existence of the recipe and its ratings
    response = client.get(f'/api/recipes/{recipe_id}/ratings/average')
    assert response.status_code != 404, "Recipe or ratings not found in the database."
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.get_json()
    assert 'averages' in data, "Averages not calculated."
    assert 'overall' in data['averages'], "Overall average not calculated."


def test_get_ratings_for_recipe_with_no_ratings(client):
    """Test retrieving ratings for a recipe that has no ratings."""
    recipe_id = 2  # Ensure this recipe ID exists but has no ratings
    response = client.get(f'/api/recipes/{recipe_id}/ratings')
    assert response.status_code == 404
    assert 'No ratings found' in response.get_json()['message']
