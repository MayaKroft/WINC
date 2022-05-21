# Do not modify these lines
__winc_id__ = '62311a1767294e058dc13c953e8690a4'
__human_name__ = 'casting'

# Add your code after this line

"""
Exercise: Casting
"""

# Part 1

# Create a variable leek_price with an integer value of 2.

leek_price = 2

# Cast this into a string and use the +-operator to print a string like this one, only with the correct price in it: 'Leek is 50 euro per kilo.'

print('Leek is ' + str(leek_price) + ' euro per kilo.')

# Part 2

# We got an order for four leeks! Store the string 'leek 4' in a variable.

order = 'leek 4'

# Use find and slicing to extract the number from this string.

order_quantity = order[order.find(' ') + 1:]

# Cast it into an integer.

order_quantity_to_int = int(order_quantity)

# Use this and leek_price to compute the sum total and store it in sum_total. Print out the value for this variable.

sum_total = leek_price * order_quantity_to_int
print(sum_total)

# Part 3
# Broccoli costs 2.34 euros per kg. We got an order: 'broccoli 1.6'.
# Create one variable for the broccoli price and one for the order.

broccoli_price = 2.34
broccoli_order = 'broccoli 1.6'
broccoli_order_to_float = float(broccoli_order[broccoli_order.find(' ') + 1:])

# Compute the total price for this order.

broccoli_order_total = broccoli_order_to_float * broccoli_price

# Use the +-operator to assemble and print a string that looks like the following: '1.6kg broccoli costs 500.34e'

print(str(broccoli_order_to_float) +'kg broccoli costs ' + str(round(broccoli_order_total, 2)) + 'e')
# Tip
# 
# You can use round(number, 2) to round number to 2 decimal places.
# 
# Wincpy Check
# Use wincpy check casting to see if you met all of the requirements for this exercise. Did you pass the test? 
