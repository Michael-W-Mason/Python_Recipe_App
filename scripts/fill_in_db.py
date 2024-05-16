import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from src.models.recipe_model import Recipes
def main():
    # Adds n number of rows with random data for front end testing only
    for i in range(50):
        recipe = Recipes.create(
            name = f'Recipe {i}',
            desc = 'asfdasd.v,nas;divunasdvnas;oviuansd[dvuiahssdvdajsndvasdjnasdiuhad[iuadv]]',
            cook_time = 2,
            serves = 4
        )
        print(recipe)

if __name__ == '__main__':
    main()