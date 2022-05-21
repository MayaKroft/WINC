# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line

"""
Assignment: Strings 
First part
"""
# Step 1 Create a variable for every player that scored.
scorer_0 = 'Ruud Gullit'
scorer_1 = 'Marco van Basten'

# Step 2: Create a variable for each minute of the match that a goal was scored.
goal_0 = 32
goal_1 = 54

# Step 3: using the + operator create a string that reports on who scored when
scorers = scorer_0 + ' ' + str(goal_0) + ', ' + scorer_1 + ' ' + str(goal_1)

# Step 4: Use f-strings or the +-operator to create a single string with information about who scored when
report = f'{scorer_0} scored in the {goal_0}nd minute\n{scorer_1} scored in the {goal_1}th minute'

"""
Assignment: Strings 
Second part
Do each exercise in a single line of code. Make sure that your code still produces the correct results for different values for the player  value.
"""
#Step 1: Choose a player that played in the soccer match and store his name as a string
player = scorer_0

#Step 2: use slicing and the find-method to isolate and store the player's first name.
first_name = player[0:player.find(' ')]

#Step3:  use find, slicing and len to isolate and store the length of their last name.
last_name_len = len(player[(player.find(' ')+1):])

#Step 4:  isolate and store the player's name
name_short = f'{first_name[0]}. {player[-last_name_len:]}'

#Step 5: First name plus '!', times the number of characters in their first name. Make sure the last character of this string is not a space! 
chant = ((first_name + '! ') * len(first_name)).rstrip()

#Step 6: Make super sure the last character of chant is NOT a SPACE
good_chant = (chant[-1] != ' ')

"""
Exercise concluded
Student X. M. van der Kroft M.
"""