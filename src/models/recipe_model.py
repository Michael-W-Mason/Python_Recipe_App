from peewee import *
from src.configs.db import db
from datetime import datetime

class BaseModel(Model):
    class Meta:
        database = db

class Recipes(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    desc = CharField()
    cook_time = FloatField()
    serves = IntegerField()
    created_at = TimestampField(default=datetime.now())
    updated_at = TimestampField(default=datetime.now())

    @staticmethod
    def get_all_recipes():
        recipes = Recipes.select(Recipes.name, Recipes.id, Recipes.desc, Recipes.cook_time, Recipes.serves)
        data = []
        for i, ele in enumerate(recipes):
            data.append({
                'id' : ele.id,
                'name' : ele.name,
                'desc' : ele.desc,
                'cook_time' : ele.cook_time,
                'serves' : ele.serves,
            })
        return data

    @staticmethod
    def get_all_information_for_recipe(id):
        # Todo: Make this into smaller queries, feel like there is a better way
        recipe = Recipes.select().where(id == Recipes.id).first()
        image = Recipe_Images.select(Recipe_Images.filename).where(id == Recipe_Images.recipe).first()
        ingredients = Ingredients.select().where(id == Ingredients.recipe).order_by(Ingredients.position)
        instructions = Instructions.select().where(id == Instructions.recipe).order_by(Instructions.position)

        data = {}
        data['name'] = recipe.name
        data['id'] = id
        data['desc'] = recipe.desc
        data['cook_time'] = recipe.cook_time
        data['serves'] = recipe.serves
        data['created_at'] = recipe.created_at
        data['image'] = image.filename
        data['ingredients'] = []
        data['instructions'] = []
        for i, ele in enumerate(ingredients):
            data['ingredients'].append(ele.ingredient)
        for i, ele in enumerate(instructions):
            data['instructions'].append(ele.instruction)   

        print(data['ingredients'])
        return data

class Ingredients(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='ingredients')
    position = IntegerField()
    ingredient = CharField()

class Instructions(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='instructions')
    position = IntegerField()
    instruction = CharField()

class Recipe_Images(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='images')
    filename = CharField(max_length=255)
