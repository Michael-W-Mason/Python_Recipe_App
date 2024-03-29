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
