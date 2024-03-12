from src import app
from src.controllers import recipe_controller
from src.configs.db import create_tables

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)