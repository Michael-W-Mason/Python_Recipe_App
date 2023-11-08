from src import app
from flask import render_template, redirect, request, session

@app.route('/')
def home():
    return render_template('recipe_form.html')

@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    print(request.form.get('recipe'))
    print(request.form.getlist('ingredient[]'))
    print(request.form.getlist('instruction[]'))
    return redirect('/')