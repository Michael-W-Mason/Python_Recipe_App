from peewee import *
from src.configs.db import db
from datetime import datetime

class BaseModel(Model):
    class Meta:
        database = db

class Recipes(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    created_at = TimestampField(default=datetime.now())
    updated_at = TimestampField(default=datetime.now())

class Ingredients(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='ingredients')
    position = IntegerField()
    ingredient = CharField()
    created_at = TimestampField(default=datetime.now())
    updated_at = TimestampField(default=datetime.now())

class Instructions(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='instructions')
    position = IntegerField()
    instruction = CharField()
    created_at = TimestampField(default=datetime.now())
    updated_at = TimestampField(default=datetime.now())

class Recipe_Image(BaseModel):
    id = PrimaryKeyField()
    recipe = ForeignKeyField(Recipes, backref='images')
    filename = CharField(max_length=255)
