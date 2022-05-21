# Do not modify these lines
__winc_id__ = '25596924dffe436da9034d43d0af6791'
__human_name__ = 'conditions'

# Add your code after this line
"""
A local farm has asked you to write a program to help them decide what to do next based on some conditions. You're going to write a function that takes factors and returns a string with one or more actions in it. The value of the factors determine what action(s) the farmer should take.

""" 

def farm_action(weather, time_of_day, cow_milking_status, location_of_cows, season, slurry_tank, grass_status):

    if (location_of_cows == 'pasture' 
    and time_of_day == 'night' 
    or location_of_cows == 'pasture' 
    and weather == 'rainy'):
        action = 'take cows to cowshed'
        return action
        
    elif cow_milking_status == True:
        if location_of_cows == 'cowshed':
            action ='milk cows'
            return action
        elif location_of_cows == 'pasture':
            action = 'take cows to cowshed\nmilk cows\ntake cows back to pasture'
            return action

    elif (slurry_tank == True 
    and weather != 'sunny' 
    and weather != 'windy'):
        if location_of_cows == 'cowshed':
            action = 'fertilize pasture'
            return action
        elif location_of_cows == 'pasture':
            action = 'take cows to cowshed\nfertilize pasture\ntake cows back to pasture'
            return action
        
    elif (grass_status == True 
    and season == 'spring' 
    and weather == 'sunny'):
        if location_of_cows == 'cowshed':
            action = 'mow grass'
            return action 
        elif location_of_cows == 'pasture':
            action = 'take cows to cowshed \nmow grass  \ntake cows back to pasture'
            return action

    else:
        action = 'wait'
        return action 





print(farm_action('rainy', 'night', False, 'cowshed', 'winter', True, True))
#'fertilize pasture'

print(farm_action('rainy', 'night', False, 'cowshed', 'winter', False, True))
#'wait'

print(farm_action('windy', 'night', True, 'cowshed', 'winter', True, True))
#'milk cows'

print(farm_action('sunny', 'day', True, 'pasture', 'spring', False, True))
#"""take cows to cowshed
#milk cows
#take cows back to pasture"""

"""
Wincpy Check
Use wincpy check conditions to see if you met all of the requirements for this exercise. Did you pass the test?
"""