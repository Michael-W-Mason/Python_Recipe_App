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
    def create_recipe(name, desc, cook_time, serves):
        recipe = Recipes()
        recipe.name = name
        recipe.desc = desc
        recipe.cook_time = cook_time
        recipe.serves = serves
        recipe.save()
        return recipe.id
    
    @staticmethod
    def delete_recipe_by_id(id):
        Recipes.delete_by_id(id)
        return id

    @staticmethod
    def update_recipe_by_id(id, name, desc, cook_time, serves):
        recipe = Recipes.get_by_id(id)
        recipe.name = name
        recipe.desc = desc
        recipe.cook_time = cook_time
        recipe.serves = serves
        recipe.updated_at = datetime.now()
        recipe.save()
        return recipe.id

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
    def get_all_information_for_recipe_by_id(id):
        # Todo: Make this into smaller queries, feel like there is a better way
        recipe = Recipes.select().where(id == Recipes.id).first()
        ingredients = Ingredients.select().where(id == Ingredients.recipe).order_by(Ingredients.position)
        instructions = Instructions.select().where(id == Instructions.recipe).order_by(Instructions.position)

        data = {}
        data['name'] = recipe.name
        data['id'] = id
        data['desc'] = recipe.desc
        data['cook_time'] = recipe.cook_time
        data['serves'] = recipe.serves
        data['created_at'] = recipe.created_at
        data['ingredients'] = []
        data['instructions'] = []
        for i, ele in enumerate(ingredients):
            data['ingredients'].append(ele.ingredient)
        for i, ele in enumerate(instructions):
            data['instructions'].append(ele.instruction)   
        return data

class Ingredients(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='ingredients')
    position = IntegerField()
    ingredient = CharField()

    @staticmethod
    def delete_all_ingredients_by_recipe_id(id):
        query = Ingredients.delete().where(Ingredients.recipe == id)
        query.execute()
        return
    
    @staticmethod
    def insert_ingredient_by_recipe_id(id, data_arr):
        for i, ele in enumerate(data_arr):
            ingredient = Ingredients()
            ingredient.recipe = id
            ingredient.position = i
            ingredient.ingredient = ele
            ingredient.save()

class Instructions(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='instructions')
    position = IntegerField()
    instruction = CharField()

    @staticmethod
    def delete_all_instructions_by_recipe_id(id):
        query = Instructions.delete().where(Instructions.recipe == id)
        query.execute()
        return
    
    @staticmethod
    def insert_instruction_by_recipe_id(id, data_arr):
        for i, ele in enumerate(data_arr):
            instruction = Instructions()
            instruction.recipe = id
            instruction.position = i
            instruction.instruction = ele
            instruction.save()
