# Do not modify these lines
from helpers import get_countries

__winc_id__ = "00a4ab32f1024f5da525307a1959958e"
__human_name__ = "dictionariesv2"

# Add your code after this line

def create_passport(name, date_of_birth, place_of_birth, height, nationality):
    passport = {
        'name': name,
        'date_of_birth': date_of_birth,
        'place_of_birth': place_of_birth,
        'height': float(height),
        'nationality': nationality
    }
    return passport


def add_stamp(submitted_passport, country):
    if submitted_passport['nationality'] != country:
        if 'stamps' in submitted_passport:
            if country not in submitted_passport['stamps']:
                submitted_passport['stamps'] += [country]  
                
        else:
            d2 = {'stamps': [country]}
            submitted_passport.update(d2)

    return submitted_passport
            

def add_biometric_data(passport, data_type_name, value_to_be_added, date):
    if 'biometric' in passport:
        update_bio = {
            data_type_name : {
                'date' : date,
                'value' : value_to_be_added
                }
            }
        passport['biometric'].update(update_bio)
    else:
        update_dict = {
            'biometric' : {
            data_type_name : {
                'date' : date,
                'value' : value_to_be_added
                }
            }
        }
        passport.update(update_dict)
    return passport

    
    