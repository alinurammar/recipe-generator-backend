# PantryPal Backend

Welcome to the backend repository for PantryPal, your intelligent culinary assistant that generates recipes based on the ingredients you have on hand. This Python Flask backend interfaces with OpenAI's GPT-3 to provide you with creative and delicious recipes, helping to reduce food waste and make cooking at home a breeze.

## Getting Started

To get started with the PantryPal backend, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the cloned repository directory.
3. Set up a virtual environment:

```bash
python3 -m venv .venv
```
4. Activate the virtual environment
```bash
source .venv/bin/activate
```
5. Create a .env file in the root directory of the project with the following content:
```bash
OPEN_API_KEY=REPLACE_WITH_YOUR_OPENAI_SECRET_KEY
```
6. Start the backend server:
```bash
make backend-run
```
The backend server will start, and you can now send requests to generate recipes.

## Running the Backend
The backend can be run locally using the provided Makefile commands:

* make init-setup: Sets up the Python virtual environment.
* make setup: Activates the Python virtual environment.
* make backend-run: Runs the Flask app.
* make requirements: Installs the required Python dependencies.
* make deploy: Deploys the app to a hosting service, such as Heroku.

## Understanding the Prompt Engineering
The backend utilizes prompt engineering to communicate with OpenAI's GPT-3 model effectively. Here's a brief overview:

* We craft a prompt that includes the ingredients provided by the user.
* Additional context, such as dietary restrictions, meal style, and desired preparation time, is appended to the prompt to tailor the recipes to the user's needs.
* The prompt is structured to instruct the AI to respond in a specific JSON format that includes a title and body for each recipe, ensuring the response is structured and easily parsed by the frontend.
* A system message is added to define the AI's role as a helpful assistant, guiding the model to generate the desired output.
* The prompt is sent to OpenAI's API, and the response is processed to extract the recipes which are then formatted and sent to the frontend.

## Additional Information
For more information on the design and architecture of the backend, or to contribute to the project, please refer to the live demo, the frontend repository, and don't hesitate to reach out to the contributors.

[Live Demo](https://recipe-generator-frontend-6f5222e90f53.herokuapp.com/)
[Frontend Repository](https://github.com/alinurammar/recipe-creator/tree/main)

We hope PantryPal inspires you in the kitchen and look forward to seeing the culinary delights you create!
