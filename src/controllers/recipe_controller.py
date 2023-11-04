from src import app
from flask import render_template, redirect, request, session

@app.route('/')
def home():
    return render_template('home.html')