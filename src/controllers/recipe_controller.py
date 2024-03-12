from src import app
from flask import render_template, redirect, request, session
from src.models.recipe_model import Recipes, Ingredients, Instructions


@app.route('/')
def home():
    return render_template('recipe_form.html')

@app.route('/recipes')
def recipes():
    all_recipes = []
    sql_recipes = Recipes()
    for recipe in Recipes.select(Recipes.id, Recipes.name):
        all_recipes.append({
            'id' : recipe.id,
            'name' : recipe.name,
        })
    return render_template('recipe_list.html', recipes=all_recipes)

@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    data = {}
    data['name']  = request.form.get('recipe')
    data['ingredients'] = request.form.getlist('ingredient[]')
    data['instructions'] = request.form.getlist('instruction[]')
    recipe = Recipes()
    recipe.name = data['name']
    recipe.save()
    for i, ele in enumerate(data['ingredients']):
        ingredient = Ingredients()
        ingredient.recipe = recipe.id
        ingredient.position = i
        ingredient.ingredient = ele
        ingredient.save()
    for i, ele in enumerate(data['instructions']):
        instruction = Instructions()
        instruction.recipe = recipe.id
        instruction.position = i
        instruction.instruction = ele
        instruction.save()
    
    return redirect('/')