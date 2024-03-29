from src import app
from flask import render_template, redirect, request, session
from werkzeug.utils import secure_filename
import os
from src.models.recipe_model import Recipes, Ingredients, Instructions, Recipe_Image

UPLOAD_FOLDER = './db/images'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes')
def recipes():
    all_recipes = []
    for recipe in Recipes.select(Recipes.id, Recipes.name):
        all_recipes.append({
            'id' : recipe.id,
            'name' : recipe.name,
        })
    return render_template('recipe_list.html', recipes=all_recipes)

@app.route('/recipes/edit/<id>')
def edit_recipe(id):
    query_1 = Recipes().select(Recipes.name).where(Recipes.id == id).first()
    query_2 = Ingredients.select().where(Ingredients.recipe == id).order_by(Ingredients.position)
    query_3 = Instructions.select().where(Instructions.recipe == id).order_by(Instructions.position)

    recipe = {}
    recipe['name'] = query_1.name
    recipe['id'] = id
    recipe['ingredients'] = []
    for i, ele  in enumerate(query_2):
        recipe['ingredients'].append(ele.ingredient)
    recipe['instructions'] = []
    for i,ele in enumerate(query_3):
        recipe['instructions'].append(ele.instruction)
    return render_template('recipe_form.html', recipe=recipe)

@app.route('/recipes/<id>')
def one_recipe(id):
    query_1 = Recipes().select(Recipes.name).where(Recipes.id == id).first()
    query_2 = Ingredients.select().where(Ingredients.recipe == id).order_by(Ingredients.position)
    query_3 = Instructions.select().where(Instructions.recipe == id).order_by(Instructions.position)
    
    recipe = {}
    recipe['name'] = query_1.name
    recipe['id'] = id
    recipe['ingredients'] = []
    for i, ele  in enumerate(query_2):
        recipe['ingredients'].append(ele.ingredient)
    recipe['instructions'] = []
    for i,ele in enumerate(query_3):
        recipe['instructions'].append(ele.instruction)
    return render_template('one_recipe.html', recipe=recipe)

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

@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    data = {}
    data['name']  = request.form.get('recipe')
    data['ingredients'] = request.form.getlist('ingredient[]')
    data['instructions'] = request.form.getlist('instruction[]')
    
    recipe = Recipes()
    recipe.name = data['name']
    recipe.save()

    if 'recipe_image' not in request.files:
        return redirect(request.url)
    file = request.files['recipe_image']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        recipe_image = Recipe_Image()
        recipe_image.recipe = recipe.id
        recipe_image.filename = filename
        recipe_image.save()
    

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS