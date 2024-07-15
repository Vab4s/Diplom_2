import random
from data.ingredients import ingredients_id
from helpers.register_random_user import generate_random_string

ingredient_choise = random.choice(ingredients_id)

def order(number_of_ingredients=random.randint(1, 3), hash=True):
    burger = list()
    if hash is True:
        for ingredient in range(number_of_ingredients):
            burger.append(random.choice(ingredients_id))
    elif hash is False:
        for ingredient in range(number_of_ingredients):
            burger.append('any_random_string_' + generate_random_string(5))
    return {"ingredients": burger}

print(order(3, False))