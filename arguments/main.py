# Do not modify these lines
__winc_id__ = '7b9401ad7f544be2a23321292dd61cb6'
__human_name__ = 'arguments'

# Add your code after this line


def main():
    print(greet('Bob', "What's up, <name>?, long time no see!"))
    print(force(75, 'moon'))
    print(pull(0.1, 5972*10**24, 6371*10**6))


# Part 1: Greet Template
# Greet should replace name in template by the name given in the 1st parameter

def greet(name, greeting='Hello, <name>!'):
    message = greeting.replace('<name>', name)
    return message


# Part 2: Force
# force=mass*gravity

planets_gravity = {
    'sun': 274,
    'jupiter': 24.9,
    'neptune': 11.2,
    'saturn': 10.4,
    'earth': 9.8,
    'uranus': 8.9,
    'venus': 8.9,
    'mars': 3.7,
    'mercury': 3.7,
    'moon': 1.6,
    'pluto': 0.6
}


def force(mass, planet='earth'):
    planet = planet.lower()
    gravity = planets_gravity[planet]
    f = mass * gravity
    return f

# Part 3: Gravity
# pull = G × ((m1×m2)/d^2)


def pull(m1, m2, d):
    g = 6.674*10**-11
    pull = g*(m1*m2/d**2)
    return pull


if __name__ == "__main__":
    main()
