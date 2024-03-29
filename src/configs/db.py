from peewee import SqliteDatabase


db = SqliteDatabase('./db/recipes.db')

def create_tables():
    from src.models.recipe_model import Recipes, Ingredients, Instructions, Recipe_Images
    with db:
        db.create_tables([Recipes, Ingredients, Instructions, Recipe_Images])