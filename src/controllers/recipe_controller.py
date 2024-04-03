from src import app
from flask import render_template, redirect, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from src.models.recipe_model import Recipes, Ingredients, Instructions

# This config is for the file uploads
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cdn/<int:id>/<path:filename>')
def cdn(id, filename):
    # Todo: Look into better way for path
    image_path = f'../db/images/{id}/'
    return send_from_directory(image_path, filename)

@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    # Todo: Add Recipe Validation
    recipe = Recipes()
    recipe.name = request.form.get('recipe_name')
    recipe.cook_time = request.form.get('recipe_time')
    recipe.serves = request.form.get('recipe_serves')
    recipe.desc = request.form.get('recipe_desc')
    recipe.save()

    # Todo: Fix Image Validation
    # Todo: Fix Paths
    file = request.files['recipe_image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = f'./db/images/{recipe.id}/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file.save(os.path.join(save_path, filename))
        recipe.image_filename = filename
        recipe.update(image_filename = filename)
        recipe.save()
    
    # Todo: Add Ingredient Validation
    for i, ele in enumerate(request.form.getlist('ingredients[]')):
        print(ele)
        ingredient = Ingredients()
        ingredient.recipe = recipe.id
        ingredient.position = i
        ingredient.ingredient = ele
        ingredient.save()
    
    # Todo: Add Instruction Validation
    for i, ele in enumerate(request.form.getlist('instructions[]')):
        print(ele)
        instruction = Instructions()
        instruction.recipe = recipe.id
        instruction.position = i
        instruction.instruction = ele
        instruction.save()
    
    return redirect('/')

@app.route('/recipes/<id>')
def one_recipe(id):
    recipe = Recipes.get_all_information_for_recipe(id)
    return jsonify(data = recipe)

@app.route('/recipes')
def recipes():
    recipes = Recipes.get_all_recipes()
    return render_template('recipe_list.html', recipes=recipes)

@app.route('/recipes/edit_recipe/<id>')
def edit_recipe(id):
    recipe = Recipes.get_all_information_for_recipe(id)
    return render_template('recipe_form.html', recipe=recipe)

@app.route('/create_recipe')
def create_recipe():
    return render_template('recipe_form.html', recipe={})

@app.route('/submit_recipe/<id>', methods=['POST'])
def submit_edited_recipe(id):
    # Kind of janky way to do this. Probably a better way to update rather than delete everything and re-insert rows. 
    query_1 = Ingredients.delete().where(Ingredients.recipe == id)
    query_1.execute()
    query_2 = Instructions.delete().where(Instructions.recipe == id)
    query_2.execute()

    data = {}
    data['id'] = id
    data['name']  = request.form.get('recipe')
    data['ingredients'] = request.form.getlist('ingredient[]')
    data['instructions'] = request.form.getlist('instruction[]')

    query_3 = Recipes.update({Recipes.name:data['name']}).where(Recipes.id == id)
    query_3.execute()

    for i, ele in enumerate(data['ingredients']):
        ingredient = Ingredients()
        ingredient.recipe = data['id']
        ingredient.position = i
        ingredient.ingredient = ele
        ingredient.save()
    for i, ele in enumerate(data['instructions']):
        instruction = Instructions()
        instruction.recipe = data['id']
        instruction.position = i
        instruction.instruction = ele
        instruction.save()

    return redirect(f'/recipes/{id}')

@app.route('/delete_recipe/<id>')
def delete_recipe(id):
    query_1 = Ingredients.delete().where(Ingredients.recipe == id)
    query_1.execute()
    query_2 = Instructions.delete().where(Instructions.recipe == id)
    query_2.execute()
    query_3 = Recipes.delete().where(Recipes.id == id)
    query_3.execute()
    return redirect('/recipes')

@app.route('/delete/<id>')
def delete_recipe_form(id):
    recipe = Recipes().select(Recipes.name, Recipes.id).where(Recipes.id == id).first()
    return render_template('delete_recipe.html', recipe=recipe)

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS