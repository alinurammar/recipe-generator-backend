from flask import request, jsonify, Response, Flask
from flask_cors import CORS, cross_origin
import json
from markupsafe import escape
import gpt_client

app = Flask(__name__)

@app.route("/")
def home_view():
        return "<h1>Recipe Generator Backend</h1>"

def process_request(request_json):
    ingredients_list_string = request_json.get('ingredients', '')
    ingredients_list = [ingredient.strip() for ingredient in ingredients_list_string.split(',')]

    includePantry = request_json.get('includePantry', '')
    strictlyIngredients = request_json.get('strictlyIngredients', '')

    selectedFilters = request_json.get('selectedFilters', {})
    
    # Extract and concatenate contents of selected filters
    meal_style = selectedFilters.get('Meal Style', [])
    dietary_restrictions = selectedFilters.get('Dietary Restrictions', [])
    meal_speed = selectedFilters.get('Meal Speed', [])

    return {
        'ingredients': ingredients_list,
        'includePantry': includePantry,
        'strictlyIngredients': strictlyIngredients,
        'meal_style': meal_style,
        'dietary_restrictions': dietary_restrictions,
        'meal_speed': meal_speed
    }


# Post request 
@app.route("/ingredients", methods=['POST'])
@cross_origin(origin='*')
def handle_ingredients():
    data = request.json
    request_obj = process_request(data)
    response =  gpt_client.generate_recipes(request_obj)
    return jsonify({'message': response})
if __name__ == '__main__':
   app.run(debug=True)