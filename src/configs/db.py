from peewee import SqliteDatabase

db = SqliteDatabase('./db/recipes.db')
db.connect()
db.close()