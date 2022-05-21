# Do not modify these lines
__winc_id__ = '6eb355e1a60f48a28a0bbbd0c88d9ab4'
__human_name__ = 'lists'

# Add your code after this line

under_case_name_list = []
under_case_winners_list = []
movie_list = []
winners_list = ['Jaws', 'Star Wars: Episode IV - A New Hope', 'E.T. the Extra-Terrestrial', 'Memoirs of a Geisha' ]
toto_album_list = ['Fahrenheit', 'The Seventh One', 'Toto XX', 'Falling in Between', 'Toto XIV', 'Old Is New']

for movie in movie_list:
    under_case_name = movie.lower()
    under_case_name_list.append(under_case_name)
for winner in winners_list:
    under_case_winner = winner.lower()
    under_case_winners_list.append(under_case_winner)


def alphabetical_order(list):
    sorted_list =sorted(list)
    return sorted_list


def won_golden_globe(movie):
    
    name_to_check = movie.lower()
    
    if name_to_check in under_case_winners_list:
        return True
    else:
        return False


""" def remove_toto_albums(list):
    
    for item in toto_album_list:
        if item in list:
            list.remove(item)
    return list """
def remove_toto_albums(list):
    i = 0
    while i< len(list):
        item= list[i]
        if list[i] in toto_album_list:
            list.remove(item)
        else:
            i = i + 1
    return list

print(remove_toto_albums(['Fahrenheit', 'Toto XX', 'a', 'v' , 'z', 'Old Is New']))

