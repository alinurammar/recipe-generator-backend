from flask import request, jsonify, Response, Flask
from flask_cors import CORS, cross_origin
import json
from markupsafe import escape
# import gpt_client

app = Flask(__name__)

@app.route("/")
def home_view():
        return "<h1>Recipe Generator Backend</h1>"

# Post request 
@app.route("/ingredients", methods=['POST'])
@cross_origin(origin='*')
def handle_ingredients():
    data = request.json
    ingredients_list_string = data.get('ingredients', '')
    filter_list_string = data.get('filters', '')
    ingredients_list = [ingredient.strip() for ingredient in ingredients_list_string.split(',')]
    response = ingredients_list
    #Note: Testing only works locally with the gpt_client commented out
    # response =  gpt_client.generate_recipes(ingredientsList=ingredients_list, filtersList=filter_list_string)
    return jsonify({'message': response})
if __name__ == '__main__':
   app.run(debug=True)