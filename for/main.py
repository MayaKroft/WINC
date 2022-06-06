from helpers import get_countries


""" Leave this untouched. Wincpy uses it to match this assignment with the
tests it runs. """
__winc_id__ = "c545bc87620d4ced81cbddb8a90b4a51"
__human_name__ = "for"


""" Write your functions here. """

# This block is only run if this file is the entrypoint; python main.py
# It is not run if it is imported as a module: `from main import *`


def shortest_names(list):
    shortest_name_list = []
    shortest_name = min(list, key=len)
    for name in list:
        if len(name) == len(shortest_name):
            shortest_name_list.append(name)
    return shortest_name_list


def amount_vowels(string):
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    num_vowels = 0
    for char in string:
        if char in vowels:
            num_vowels = num_vowels + 1
    return num_vowels


def most_vowels(list):
    return sorted(list, key=amount_vowels, reverse=True)[:3]


def alphabet_set(list):
    completing_list = []
    list_to_analyze = list
    remaining_alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'
        ]

    def unique_chars(name):
        unique_characters = []
        number_unique_character = 0
        lowecase_name = name.lower()
        for letter in lowecase_name:
            if (letter != ' '
               and letter not in unique_characters
               and letter in remaining_alphabet):
                unique_characters.append(letter)
                number_unique_character = number_unique_character + 1
        return number_unique_character

    def most_unique_chars(list):
        most_unique_chars = sorted(list, key=unique_chars, reverse=True)[0]
        return most_unique_chars

    def new_alphabet(name, letters):
        name = str(name).lower()
        new_letters = letters
        for letter in name:
            if letter in new_letters and letter != ' ':
                new_letters.remove(letter)
        return new_letters

    while len(remaining_alphabet) > 0:
        most = most_unique_chars(list_to_analyze)
        list_to_analyze.remove(most)
        completing_list.append(most)
        remaining_alphabet = new_alphabet(most, remaining_alphabet)
        print(most)
        print(remaining_alphabet)

    return completing_list


if __name__ == "__main__":
    countries = get_countries()

    """ Write the calls to your functions here. """


def main():
    shortest_names(countries)
    print(shortest_names(countries))
    print(amount_vowels('potato'))
    print(most_vowels(countries))
    print(alphabet_set(countries))
