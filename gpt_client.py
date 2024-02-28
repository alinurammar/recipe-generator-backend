# import the OpenAI Python library for calling the OpenAI API
import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from dotenv import load_dotenv
import os
import constants

load_dotenv()

secret_key = os.getenv('OPEN_API_KEY')

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def get_gpt_response(messages, model=constants.GPT_MODEL, max_tokens=constants.MAX_TOKENS, temperature=constants.TEMPERATURE):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + secret_key,
    }
    json_data = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def verify_response_format(response):
    try:
        # Parse the response JSON
        response_data = json.loads(response)
        
        # Check if 'recipes' key exists and it's a list
        if 'recipes' not in response_data or not isinstance(response_data['recipes'], list):
            return False
        
        # Check the format of each recipe
        for recipe in response_data['recipes']:
            if not all(key in recipe for key in ['title', 'body']):
                return False
        
        return True
    except json.JSONDecodeError:
        return False
    
# Function to convert response data to frontend format
def convert_to_frontend_format(response_data):
    # Initialize a list to store recipes
    recipes = []
    data = json.loads(response_data)
    for idx, recipe in enumerate(data['recipes']):
        formatted_recipe = {}
        for key, value in recipe.items():
            if key in ['title', 'body']:
                formatted_recipe[key] = value
            else:
                formatted_recipe[key] = value.replace('\n', '')

        frontend_recipe = {
            "id": idx + 1,
            "title": formatted_recipe['title'],
            "body": formatted_recipe['body']
        }
        recipes.append(frontend_recipe)

    return recipes

def generate_recipes(request_data):
    try:
        chat_response = get_gpt_response(build_prompt(request_data))
        recipes = extract_recipes(chat_response)
        isCorrectFormat = verify_response_format(recipes)
        if isCorrectFormat:
            convertedResponse = convert_to_frontend_format(recipes)
            return convertedResponse
        else:
            return ""

    except Exception as e:
        print(f"Error generating recipes: {e}")
        return None

def build_prompt(request_data):
    ingredients = request_data['ingredients']
    
    pantry_items = constants.pantry_and_spice_ingredients
    
    # Check if includePantry flag is True, then add pantry ingredients
    if request_data.get('includePantry', False):
        pantry_prompt = f"You may assume we have the following ingredients in our pantry: {', '.join(pantry_items)}. Ignore non food items\n"
    else:
        pantry_prompt = ""

    return_format = "Respond with your analysis in JSON format. The JSON schema should be a list of " + str(constants.JSON_SCHEMA)
    prompt = f"Generate 3 recipes using the following ingredients: {', '.join(ingredients)}. {pantry_prompt}"

    # Check if there are any meal styles specified
    meal_styles = request_data.get('meal_style', [])
    if meal_styles:
        prompt += "Make sure the recipes are suitable for "
        for style in meal_styles:
            prompt += f"{style.lower()} "
        prompt += "meals. "
    
    # Check if there are any dietary restrictions specified
    dietary_restrictions = request_data.get('dietary_restrictions', [])
    if dietary_restrictions:
        prompt += "Ensure the recipes are "
        for restriction in dietary_restrictions:
            prompt += f"{restriction.lower()} "
        prompt += "friendly. "

    # Check if there are any meal speeds specified
    meal_speeds = request_data.get('meal_speed', [])
    if meal_speeds:
        prompt += "Try to keep the recipes to a "
        for speed in meal_speeds:
            prompt += f"{speed.lower()} "
        prompt += "preparation time. "

    
    prompt += return_format
    messages = [{"role": "system", "content": "You are a helpful assistant that provides concise recipes."}]
    messages.append({"role": "user", "content": prompt})
    
    return messages


def extract_recipes(chat_response):    
    response = chat_response.json()["choices"][0]["message"]["content"]
    return response
