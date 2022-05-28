from curses.ascii import isdigit
from email import message
from operator import ge
from helpers import random_koala_fact

__winc_id__ = "c0dc6e00dfac46aab88296601c32669f"
__human_name__ = "while"

# This block is only executed if this script is run directly (python main.py)
# It is not run if you import this file as a module.

        
def main(): 
    print(random_koala_fact())
    print(unique_koala_facts(3))
    print(num_joey_facts())
    print(koala_weight())


def unique_koala_facts(i):
    if i < 1000:
        a = 0
        unique_fact_list =[]
        while len(unique_fact_list) < i or a < i:
            fact = random_koala_fact()
            if fact not in unique_fact_list:
                unique_fact_list.append(fact)
            a = a + 1
        return unique_fact_list
    else:  
        message = 'limit surpassed'
        return message


def get_joey_facts():
    fact_found = False

    while fact_found == False:
        koala_fact = random_koala_fact()
        if 'joey' in koala_fact.lower():
            joey_fact = koala_fact
            fact_found = True
        else: 
            continue
    return joey_fact

def num_joey_facts():
    unique_joey_fact_list =[]
    repetition_list = []
    while 10 not in repetition_list:
        joey_fact = get_joey_facts()
        if joey_fact not in unique_joey_fact_list:
            unique_joey_fact_list.append(joey_fact)
            repetition_list.append(joey_fact)
            repetition_list.append(1)
            #print('new fact')
        else: 
            fact_index = repetition_list.index(joey_fact)
            repetition_index = fact_index + 1
            repetition_list[repetition_index] = repetition_list[repetition_index] +1
            #print(f'old fact current repetitions {repetition_list[repetition_index]}')

    return len(unique_joey_fact_list)

def get_weight_fact():
    w_fact_found = False
    while w_fact_found == False:
        koala_fact = random_koala_fact()
        if 'kg' in koala_fact.lower():
            weight_fact = koala_fact
            w_fact_found = True
        else: 
            continue
    return weight_fact
    


def koala_weight():
    weight_fact_found = False
    while(weight_fact_found == False):
        w_fact = get_weight_fact()
        for a in w_fact.split():
            if 'kg' in a:
                weight = int(a[:a.index('k')])     
                weight_fact_found = True
        else:
            continue
    return weight



if __name__ == "__main__":
    main()