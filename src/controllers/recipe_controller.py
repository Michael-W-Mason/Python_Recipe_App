from src import app
from flask import render_template, redirect, request, jsonify, send_from_directory
import os
from src.models.recipe_model import Recipes, Ingredients, Instructions


ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
IMAGE_PATH = f'./db/images/'

@app.route('/recipe_app/')
def home():
    recipes = Recipes.get_last_n_recipes(3)
    return render_template('home.html', recipes=recipes)

@app.route('/recipe_app/recipes/')
@app.route('/recipe_app/recipes/<int:page>')
def recipes(page = 1):
    recipes = Recipes.paginate_recipes(page)
    return render_template('recipe_list.html', recipes=recipes, page=page)

@app.route('/recipe_app/recipes/search', methods=['POST'])
def search_recipes(page = 1):
    query = request.form.get('search')
    recipes = Recipes.search_recipes(query=query)
    if query == '':
        return redirect('/recipe_app/recipes')
    return render_template('recipe_list.html', recipes=recipes, page=page)

@app.route('/recipe_app/submit_recipe', methods=['POST'])
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

    return redirect('/recipe_app/recipes')

@app.route('/recipe_app/recipes/get_recipe/<int:id>')
def one_recipe(id):
    recipe = Recipes.get_all_information_for_recipe_by_id(id)
    return jsonify(data = recipe)


@app.route('/recipe_app/recipes/edit_recipe/<int:id>')
def edit_recipe(id):
    recipe = Recipes.get_all_information_for_recipe_by_id(id)
    return render_template('recipe_form.html', recipe=recipe)

@app.route('/recipe_app/create_recipe')
def create_recipe():
    return render_template('recipe_form.html', recipe={})

@app.route('/recipe_app/delete_recipe/<int:id>')
def delete_recipe(id):
    Instructions.delete_all_instructions_by_recipe_id(id)
    Ingredients.delete_all_ingredients_by_recipe_id(id)
    Recipes.delete_recipe_by_id(id)
    return redirect('/recipes')

@app.route('/recipe_app/submit_recipe/<int:id>', methods=['POST'])
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

    return redirect(f'/recipe_app/recipes')

@app.route('/recipe_app/cdn/<int:id>')
def cdn(id):
    # Probably a better way to do this? Probably store file extension or filename in db?
    # Hard to deal with multiple allowed file extensions, could turn all uploaded images to jpeg???
    if id == 0:
        return send_from_directory('../db/images/', 'default.jpg')
    for path, dirs, images in os.walk(IMAGE_PATH):
        for image in images:
            recipe_id = image.split('.')[0]
            if recipe_id == str(id):
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
    return


def save_file(file, recipe_id):
    file_extension = file.filename.split('.')[1]
    file.filename = f'{recipe_id}.{file_extension}'
    check_if_file_exists_and_delete(recipe_id)
    file.save(os.path.join(IMAGE_PATH, file.filename))
    return
