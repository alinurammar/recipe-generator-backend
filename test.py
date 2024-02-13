import app

# Test data
ingredientsAndSelectedFiltersTest = {
    "ingredients": "Quinoa, Lettuce, Onion, Tomatoes, Chicken, Honey",
    "filters": {
        "Meal Style": [
            "Breakfast"
        ],
        "Dietary Restrictions": [
            "Halal"
        ],
        "Meal Speed": [
            "1 hr"
        ]
    }
}

ingredientsTest = {
    "ingredients": "Quinoa, Lettuce, Onion, Tomatoes, Chicken, Honey"
}

ingredientsAndPantryTest = {
    "ingredients": "Quinoa, Lettuce, Onion, Tomatoes, Chicken, Honey",
    "includePantry": False
}

ingredientsAndStrictIngredientsTest = {
    "ingredients": "Quinoa, Lettuce, Onion, Tomatoes, Chicken, Honey",
    "strictlyIngredients": True
}

# Function to test the handle_ingredients function
def test_handle_ingredients(data):
    with app.app.test_request_context('/', json=data, method='POST'):
        response = app.handle_ingredients()
        print(f"Test Data: {data}")
        print(f"Response JSON: {response.get_json()}")

# Run tests
test_handle_ingredients(ingredientsAndSelectedFiltersTest)
test_handle_ingredients(ingredientsTest)
test_handle_ingredients(ingredientsAndPantryTest)
test_handle_ingredients(ingredientsAndStrictIngredientsTest)
