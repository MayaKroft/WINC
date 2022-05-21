# Do not modify these lines
__winc_id__ = '49bce82ef9cc475ca3146ee15b0259d0'
__human_name__ = 'functions'

# Add your code after this line

""" 
Define these functions in main.py:
""" 
# greet: takes a name and returns a string in the format: greet('Bob') 'Hello, Bob!'

def greet(x):
 greeting = f'Hello, {x}!'
 return greeting

print(greet('Bob'))

# add: takes three numbers (integers or floats) and returns their sum. 

def add(x,y,z):
 addition = x + y + z
 return addition

print(add(5,3,2))


# positive: takes a number (integer or float) and returns whether or not it is positive in the form of a boolean. You do not have to handle the case where the argument is not an int or a float.

def positive(x):
 if x > 0:
  is_positive = True
  return is_positive
 else:
  is_positive = False
  return is_positive

print(positive(50))
print(positive(0))
print(positive(-50))


"""
negative: takes a number (integer or float) and returns whether or not it is negative in the form of a boolean. You do not have to handle the case where the argument is not an int or float. Examples:

>>> negative(50)
False
>>> negative(-50)
True
>>> negative(0)
False
""" 

def negative(x):
 if x < 0:
  is_negative = True
  return is_negative
 else:
  is_negative = False
  return is_negative

print(negative(50))
print(negative(0))
print(negative(-50))
"""Wincpy Check
Use wincpy check functions to see if you met all of the requirements for this exercise. Did you pass the test? """

