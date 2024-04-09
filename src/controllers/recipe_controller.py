from src import app
from flask import render_template, redirect, request, jsonify, send_from_directory
import os
from src.models.recipe_model import Recipes, Ingredients, Instructions


ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
IMAGE_PATH = f'./db/images/'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    # Todo: Add Recipe Validation
    recipe_id = Recipes.create_recipe(
        name=request.form.get('name'),
        desc=request.form.get('desc'),
        cook_time=request.form.get('cook_time'),
        serves=request.form.get('serves'),
    )
    # Todo: Fix Image Validation
    file = request.files['recipe_image']
    if file:
        save_file(file, recipe_id)

    # Todo: Add Ingredient Validation
    Ingredients.insert_ingredient_by_recipe_id(recipe_id, request.form.getlist('ingredients[]'))
    # Todo: Add Instruction Validation
    Instructions.insert_instruction_by_recipe_id(recipe_id, request.form.getlist('instructions[]'))    

    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def one_recipe(id):
    recipe = Recipes.get_all_information_for_recipe_by_id(id)
    return jsonify(data = recipe)

@app.route('/recipes')
def recipes():
    recipes = Recipes.get_all_recipes()
    return render_template('recipe_list.html', recipes=recipes)

@app.route('/recipes/edit_recipe/<int:id>')
def edit_recipe(id):
    recipe = Recipes.get_all_information_for_recipe_by_id(id)
    return render_template('recipe_form.html', recipe=recipe)

@app.route('/create_recipe')
def create_recipe():
    return render_template('recipe_form.html', recipe={})

@app.route('/submit_recipe/<int:id>', methods=['POST'])
def submit_edited_recipe(id):
    # Kind of janky way to do this. Probably a better way to update rather than delete everything and re-insert rows. 
    Ingredients.delete_all_ingredients_by_recipe_id(id)
    Instructions.delete_all_instructions_by_recipe_id(id)


    recipe_id = Recipes.update_recipe_by_id(
        id=id,
        name=request.form.get('name'),
        desc=request.form.get('desc'),
        cook_time=request.form.get('cook_time'),
        serves=request.form.get('serves'),
    )

    file = request.files['recipe_image']
    if file:
        save_file(file, recipe_id)

    Ingredients.insert_ingredient_by_recipe_id(id, request.form.getlist('ingredients[]'))
    Instructions.insert_instruction_by_recipe_id(id, request.form.getlist('instructions[]'))

    return redirect(f'/recipes')

@app.route('/cdn/<int:id>')
def cdn(id):
    # Probably a better way to do this? Probably store file extension or filename in db?
    # Hard to deal with multiple allowed file extensions, could turn all uploaded images to jpeg???
    if id == 0:
        return send_from_directory('../db/images/', 'default.jpg')
    for path, dirs, images in os.walk(IMAGE_PATH):
        for image in images:
            recipe_id = image.split('.')[0]
            print(recipe_id, id, image)
            if recipe_id == str(id):
                print(image)
                return send_from_directory('../db/images/', image)
    return send_from_directory('../db/images/', 'default.jpg')

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_if_file_exists_and_delete(recipe_id):
    # Really need better solution than this... But it works!
    for path, dirs, images in os.walk(IMAGE_PATH):
        for image in images:
            if image.split('.')[0] == recipe_id:
                os.remove(f'{path}/{image}')
                continue
    return


def save_file(file, recipe_id):
    file_extension = file.filename.split('.')[1]
    file.filename = f'{recipe_id}.{file_extension}'
    check_if_file_exists_and_delete(recipe_id)
    file.save(os.path.join(IMAGE_PATH, file.filename))
    return
