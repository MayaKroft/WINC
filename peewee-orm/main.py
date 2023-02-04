import models
import peewee
from typing import List

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    cheapest= models.Dish.select().where(peewee.fn.MIN(models.Dish.price_in_cents))
    return cheapest


def vegetarian_dishes() -> List[models.Dish]:

    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """

    veg_dishes = []
    for dish in models.Dish.select():
        veg_ings = 0
        non_veg = 0
        for ingredient in dish.ingredients:
            if ingredient.is_vegetarian == True:
                veg_ings += 1
            else:
                non_veg +=1
        if veg_ings > 0 and non_veg == 0:
            veg_dishes.append(dish)
        else:
            pass
    if len(veg_dishes) > 0:
        return veg_dishes
    else:
        return None
        
    
    


def best_average_rating() -> models.Restaurant:

    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    restaurant_dict = {}
    for restaurant in models.Restaurant.select():
        ratings = []
        for rating in models.Rating.select():
            if (restaurant == rating.restaurant):
                ratings.append(rating.rating)
        average_rating = sum(ratings)/len(ratings)
        restaurant_dict[restaurant.name] = average_rating 
    if len(restaurant_dict) > 0:
        best_rating = max(list(restaurant_dict.values()))
        best_rating_index = list(restaurant_dict.values()).index(best_rating)
        best_rating_name = list(restaurant_dict.keys())[best_rating_index]
        best_rating_restaurant = models.Restaurant.select().where(models.Restaurant.name == best_rating_name)
    
    return best_rating_restaurant



def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    
    models.Rating.create(restaurant = 1 , rating = 4.5 )


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
    def vegan_options(restaurant):
        vegan_options = []
        dishes = list(models.Dish.select().where(models.Dish.served_at == restaurant))
        for dish in dishes:
            ingredients = list(dish.ingredients)
            vegan_ingredients = [i for i in ingredients if i.is_vegan == True]
            #dish.ingredients.select().where(models.Ingredient.is_vegan == True)
            #dish.ingredients.select().where(models.Ingredient.is_vegan == False)
            non_vegan_ingredients = [i for i in ingredients if i.is_vegan == False]
            if len(non_vegan_ingredients) > 0:
                pass
            elif len(vegan_ingredients) >0 and not non_vegan_ingredients:
                vegan_options.append(dish)
        if vegan_options:
            return True
        else:
            return False
    
    possible_opening = list(models.Restaurant.select().where(
        models.Restaurant.opening_time.hour <= 19 
        and 
        models.Restaurant.closing_time.hour > 19))

    possible_vegan= [i for i in possible_opening if vegan_options(i)]
    
    return possible_vegan
    
    
def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    def valid_ingredient(name, is_vege, is_vega, is_glut_free):
        models.Ingredient.get_or_create(name = name, is_vegetarian = is_vege, is_vegan = is_vega, is_glutenfree = is_glut_free)

        ing = models.Ingredient.select().where(models.Ingredient.name == name)
        
        return ing[0]

    ingredient_1 =  valid_ingredient('potato', True, True, True)

    ingredient_2 = valid_ingredient('cheese', True, False, True)

    ingredient_3 = valid_ingredient('salt', True, True, True)

    ing_list  = [ingredient_1.id, ingredient_2.id,ingredient_3.id]

    models.Dish.create(name = 'Cheesy potato', served_at= 1, price_in_cents = 450) 

    dish_m = models.Dish.select().where(models.Dish.name == 'Cheesy potato')
    dish_m[0].ingredients.add(ing_list)

    dish_m = models.Dish.select().where(models.Dish.name == 'Cheesy potato')

    return dish_m[0]
