import os
import csv
import math
import json
import getdate
import datetime
import pandas as pd
from rich import box
from rich.text import Text
from rich.table import Table
from rich.console import Console
from to_from_ymd import to_ymd, from_ymd, convert_to_ymd_txt, get_date_format


"""
This file will handle readind and writing CSV files, 
as well as a choice to grab a pre existing CSV, JSON or XLS file 
to convert it's information to the programs CSV format plus doing most of the data handling that is gotten or passed through to documents

------INDEX--------
CLASSES ---------------------------------------    42-69

BASIC FILE FUNCTIONS---------------------------    70-112

INFO GETTERS-----------------------------------    113-733

REPORT SECTION---------------------------------    733-1436

BUY ACTION HANDLING----------------------------    1438-1364

PRICE ACTION HANDLING--------------------------    1465-1492

SELL ACTION HANDLING---------------------------    1493-1566

SAVE ACTION HANDLING---------------------------    1567-1650
 
CLASS LIST MAKERS------------------------------    1651-1779

RETRIEVING INFORMATION FROM AN EXTERNAL FILE---    1780-1919
"""
CONSOLE = Console()
class ItemById:
    def __init__(self, id, name, amount, buy_price, buy_date, expiration, sale_price, sold, remaining, expired, profit):
        self.id = id
        self.name = name
        self.amount = amount
        self.buy_price = buy_price
        self.buy_date = buy_date
        self.expiration = expiration
        self.sale_price = sale_price
        self.sold = sold
        self.remaining = remaining
        self.expired = expired
        self.profit = profit

class ItemByName:
    def __init__(self, name, amount, buy_price, buy_date, expiration, sale_price, sold, remaining, expired, profit):
        self.name = name
        self.amount = amount
        self.buy_price = buy_price
        self.buy_date = buy_date
        self.expiration = expiration
        self.sale_price = sale_price
        self.sold = sold
        self.remaining = remaining
        self.expired = expired
        self.profit = profit


#--------------------- HANDLING SOME BASIC FILE FUNCTIONS ---------------------#
def dict_list_csv(file):
    dict_list = []
    try:
        with open(file, 'r', newline='') as read_file:
                reader = csv.DictReader(read_file)
                for row in reader:
                    dict_list.append(row)
                return dict_list
    except:
        file = os.path.abspath(f'superpy\{file}')
        with open(file, 'r', newline='') as read_file:
                reader = csv.DictReader(read_file)
                for row in reader:
                    dict_list.append(row)
                return dict_list

def backup_csv(file,date = False):
    date = from_ymd(date) if date else date
    CONSOLE.print('The original file will be backed up with the original name + _backup')
    original = dict_list_csv(file)
    backup_name = file[:len(file)-4] + '_backup_' + date +'.csv'
    backup_path = os.path.join('backup',backup_name)
    if original:
        with open(backup_path, 'w') as backup_file:
            writer = csv.DictWriter(backup_file, fieldnames= original[0].keys()) 
            writer.writeheader() 
            writer.writerows(original)  
        CONSOLE.print(f'Backup completed and saved to {backup_path}')
    else:
        CONSOLE.print('There was no data to backup')

def wipe_csv(file,date, headers = False):
    headers = headers if headers else list(pd.read_csv(file).columns)
    backup_csv(file, date)
    f = open(file, "w+")
    f.close()
    with open(file,'w') as fh:
        writer= csv.DictWriter(fh, fieldnames= headers)
        writer.writeheader()
    CONSOLE.print("Wipe out completed")


# ------------------------------- INFO GETTERS --------------------------------#
def get_last_id(document): #not with dict_list_csv() because it consider the possibility of no data yet
    if document == 'bought.csv':
         with open('bought.csv', newline='', mode="r") as buying_file:
            reader = csv.DictReader(buying_file)
            data = [row for row in reader]
            if data:
                ids= [int(i['id']) for i in data]
                max_id = max(ids)
                buying_file.close()
                return int(max_id)
            else:
                buying_file.close()
                return 0
    if document == 'sold.csv':
         with open('sold.csv', newline='', mode="r") as selling_file:
            reader = csv.DictReader(selling_file)
            data = [row for row in reader]
            if data:
                ids= [int(i['sell_id']) for i in data]
                max_id = max(ids)
                selling_file.close()
                return int(max_id)
            else:
                selling_file.close()
                return 0

def is_valid_id(id, date = 0):
    id = id if isinstance(id, int) else int(id)
    bought = dict_list_csv('bought.csv')
    is_valid = False
    if date:
        for item in bought:
            if int(item['id']) == id and to_ymd(item['buy_date']) <= date:
                is_valid = True
            else:
                continue
        return is_valid
    else:
        for item in bought:
            if int(item['id']) == id:
                is_valid = True
            else:
                continue
        return is_valid

def is_valid_item(item, date = 0):
    is_valid = False
    bought = dict_list_csv('bought.csv')
    if date:
        for i in bought:
            if i['product_name'] == item:
                if to_ymd(i['buy_date']) <= date:
                    is_valid = True
                else:
                    continue
            else:
                continue
        return is_valid
    else:
        for i in bought:
            if i['product_name'] == item:
                is_valid = True
            else:
                continue
            return is_valid

def get_name(id):
    id = id if isinstance(id, int) else int(id)
    bought = dict_list_csv('bought.csv')
    name= False
    for item in bought:
        if int(item['id']) == id:
            name = item['product_name']
        else:
            continue
    if name:
        return name

def last_sale_price(id, given_date): #This function searches the price history of the item
    #up to and including the current date for the latest price of the item
    id = id if type(id) == int else int(id)
    given_date = to_ymd(given_date) if isinstance(given_date, str) else given_date
    price_history = dict_list_csv('prices.csv')
    last_price = 0
    price_dates = []

    for item in price_history:
        if int(item['id']) == id:
            if to_ymd(item['price_date']) <= given_date:
                price_dates.append(to_ymd(item['price_date']))

    for item in price_history:
        if int(item['id']) == id:
            if price_dates and to_ymd(item['price_date']) == max(price_dates):
                last_price = float(item['price'])

    return last_price

def last_buy_price(id, given_date): #This function searches the buy price history of the item
    #up to and including the current date for the latest price of the item
    id = id if type(id) == int else int(id)
    given_date = to_ymd(given_date) if isinstance(given_date, str) else given_date
    bought = dict_list_csv('bought.csv')
    last_buy_price = 0
    last_date = None
   
    for item in bought:
        if int(item['id']) == id:
            if to_ymd(item['buy_date']) <= given_date:
                if last_date:
                    if to_ymd(item['buy_date']) >= last_date:
                        last_buy_price = float(item['buy_price'])
                        last_date = to_ymd(item['buy_date'])
                    else:
                        last_buy_price = float(item['buy_price'])
                else:
                    last_date = to_ymd(item['buy_date'])
                    last_buy_price = float(item['buy_price'])
    return last_buy_price

def amount_sold(id, end_date, start_date= 0): 
    id = id if isinstance(id, int) else int(id)
    sold = dict_list_csv('sold.csv')
    amount_sold = 0
    for item in sold:
        sell_date = to_ymd(item['sell_date'])
        if int(item['id']) == id:
            if start_date:
                if sell_date <= end_date and sell_date >= start_date:
                    amount_sold += int(item['amount_sold'])
            else:
                if sell_date <= end_date:
                    amount_sold += int(item['amount_sold'])
    return amount_sold

def get_total_revenue(id, end_date, start_date= 0):
    id = id if isinstance(id, int) else int(id)
    sold = dict_list_csv('sold.csv')
    total_revenue = 0.0
    if start_date:
        for item in sold:
            sell_date = to_ymd(item['sell_date'])
            if int(item['id']) == id:
                if sell_date <= end_date and sell_date >= start_date:
                    total_revenue += (float(item['sell_price']) * int(item['amount_sold']))
        return round(total_revenue, 2)

    else:
        for item in sold:
            sell_date = to_ymd(item['sell_date'])
            if int(item['id']) == id:
                if sell_date <= end_date:
                    total_revenue += (float(item['sell_price']) * int(item['amount_sold']))
        return total_revenue

def get_total_cost(id,end_date,start_date= 0):
    id = id if isinstance(id, int) else int(id)
    bought = dict_list_csv('bought.csv')
    if start_date:
        total_cost = 0
        bought_on_range = []
        for i in bought:
            if int(i['id']) == id:
                if to_ymd(i['buy_date']) >= start_date and to_ymd(i['buy_date']) <= end_date:
                    bought_on_range.append(i)
            else:
                pass
        for b in bought_on_range:
            total_cost +=  float(b['buy_price']) * int(b['amount'])
        return total_cost
        
        #if start_date == end_date:
        #    total_cost = (last_buy_price(id, end_date) * amount_sold(id, end_date, start_date))
        #    return total_cost
        #else:
        """ total_cost = 0.0
        for b_item in bought:
            buy_date = to_ymd(b_item['buy_date'])
            if int(b_item['id']) == id and buy_date >= start_date and buy_date <= end_date:
                total_cost += (float(b_item['buy_price']) * int(b_item['amount'])) """

    else:
        total_cost = 0.0
        for b_item in bought :
            buy_date = to_ymd(b_item['buy_date'])
            if int(b_item['id']) == id and buy_date <= end_date:
                total_cost += (float(b_item['buy_price']) * int(b_item['amount']))
        return total_cost


def get_total_profit(id,end_date,start_date= 0):
    id = id if isinstance(id, int) else int(id)
    bought = dict_list_csv('bought.csv')
    if start_date:
        total_revenue = get_total_revenue(id, end_date, start_date)
        total_cost = get_total_cost(id, end_date, start_date)
        total_profit = total_revenue - total_cost
        

    else:
        total_revenue = get_total_revenue(id, end_date)
        total_cost = 0.0
        for b_item in bought:
            if int(b_item['id']) == id:
                total_cost += (float(b_item['buy_price']) * int(b_item['amount']))
        total_profit = total_revenue - total_cost
    
    return round(total_profit, 2)



def check_amount(id, current_date):
    #make sure it is a valid id
    id = id if type(id) == int else int(id) #just making sure the type is always right
    current_date = current_date if isinstance(current_date, datetime.date) else to_ymd(current_date)
    bought = dict_list_csv('bought.csv')
    for item in bought:
        if int(item['id']) == id:
            bought = int(item['amount'])
    sold= amount_sold(id, current_date)
    remaining = bought - sold
    return remaining

def get_id_list(product_name):
    id_list = []
    bought = dict_list_csv('bought.csv')
    for item in bought:
        if item['product_name'] == product_name:
                        id = int(item['id'])
                        id_list.append(id)
    return id_list

def get_available(date, sold_amount, id = 0, item = ''):
    date = to_ymd(date) if isinstance(date, str) else date
    id = int(id) if isinstance(id, str) else id
    sold_amount = int(sold_amount) if isinstance(sold_amount, str) else sold_amount
    if id:
        id = id if type(id) == int else int(id)
        are_remaining= True if check_amount(id, date) >= sold_amount else False
        if are_remaining:
            return id 
        else:
            CONSOLE.print(f'There are not enough items available of ID= {id}')
            CONSOLE.print('The program will search for products with a matching name to the given id')
            product_name = get_name(id)
            return get_available(date, sold_amount, item= product_name)
            #ADD PROGRESS BAR

    elif item:
        options_total = 0
        product_name = item
        possible_ids = get_id_list(product_name)
        available_ids = []
        available_amounts = []
        available_table = Table(title= f'Available {product_name} items')
        available_table.add_column('ID', style='bold white')
        available_table.add_column('Remaining', style= 'chartreuse3')
        
        for i in possible_ids: 
            is_valid = is_valid_id(i,date)
            amount = check_amount(i, date)
            if is_valid and (amount > 0):
                available_table.add_row(str(i),str(amount))
                available_ids.append(i)
                available_amounts.append(amount)
                options_total += amount
        
        if available_ids and len(available_ids) == 1:
            return available_ids[0]

        elif available_ids and (options_total > sold_amount):
            available_table.show_footer = True
            available_table.columns[-1].footer = str(sum([int(cell) for cell in available_table.columns[-1].cells]))
            CONSOLE.print(available_table)
            list_string = input('Please select the IDs followed by the amounts, separated by spaces: ')
            split_list = list_string.split()
            int_list = [int(i) for i in split_list]
            tuppled_list = []
            index= 0
            for i in range(int((len(int_list))/2)):
                tuppled_list.append(tuple([int_list[index],int_list[index+1]]))
                index +=2
            amount_given = sum([i[1] for i in tuppled_list])
            if not amount_given == sold_amount:
                CONSOLE.print(f'The amount required was {sold_amount} but {amount_given} was given, please repeat the sale request')
                return False
            else:
                return tuppled_list

        elif available_ids and (options_total == sold_amount):
            CONSOLE.print('All items are required, the sale will now proceed')
            to_sell = list(zip(available_ids, available_amounts))
            return to_sell
        elif available_ids and options_total < sold_amount:
            CONSOLE.print(available_table)
            CONSOLE.print(f'There are not enough {product_name} items in the store, \n    {sold_amount} were requested but only {options_total} are available,\n    please repeat the sale request-')
            return False
        else:
            CONSOLE.print(f'There are no {product_name} items available, please make a new request')
            return False

def make_classlist(instance, new_value):
    new_list = []
    if type(instance) == list:
        for item in instance:
            new_list.append(item)
        new_list.append(new_value)
        return new_list
    else:
        new_list.append(instance)
        new_list.append(new_value)
        return new_list

def id_buy_history(id, start_date, end_date):
    id = id if isinstance(id, int) else int(id)
    id_buy_history = {} 
    bought= dict_list_csv('bought.csv')
    if start_date == end_date or start_date == 0:
        for buy in bought:
            if id == int(buy['id']):
                buy_date = to_ymd(buy['buy_date'])
                buy_str_date= buy['buy_date']
                if buy_date <= end_date:
                    if buy_str_date not in list(id_buy_history.keys()):
                        id_buy_history[buy_str_date] = {'price': float(buy['buy_price']), 'amount': int(buy['amount'])}
                    else:
                        if isinstance(id_buy_history[buy_str_date], dict):
                            id_buy_history[buy_str_date] = [id_buy_history[buy_str_date]] + [{'price': float(buy['buy_price']), 'amount': int(buy['amount'])},]
                        elif isinstance(id_buy_history[buy_str_date], list):
                            id_buy_history[buy_str_date] += [{'price': float(buy['buy_price']), 'amount': int(buy['amount'])},]
                else:
                    continue
            else:
                continue
    else:
        for buy in bought:
            if id == int(buy['id']):
                buy_date = to_ymd(buy['buy_date'])
                buy_str_date= buy['buy_date']
                if buy_date >= start_date and buy_date<= end_date:
                    if buy_str_date not in list(id_buy_history.keys()):
                        id_buy_history[buy_str_date] = {'price': float(buy['buy_price']), 'amount': int(buy['amount'])}
                    else:
                        if isinstance(id_buy_history[buy_str_date], dict):
                            id_buy_history[buy_str_date] = [id_buy_history[buy_str_date]] + [{'price': float(buy['buy_price']), 'amount': int(buy['amount'])},]
                        elif isinstance(id_buy_history[buy_str_date], list):
                            id_buy_history[buy_str_date] += [{'price': float(buy['buy_price']), 'amount': int(buy['amount'])},]
                else:
                    continue
            else:
                continue
    return id_buy_history

def id_sale_history(id, start_date, end_date):
    id = id if isinstance(id, int) else int(id)
    id_sale_history = {}
    sales = dict_list_csv('sold.csv')
    if start_date == end_date or start_date == 0:
        for sale in sales:
            if id == int(sale['id']):
                sale_date = to_ymd(sale['sell_date'])
                sale_str_date= sale['sell_date']
                if sale_date <= end_date:
                    if sale_str_date not in list(id_sale_history.keys()):
                        id_sale_history[sale_str_date] = {'sale_price': float(sale['sell_price']), 'amount': int(sale['amount_sold']), 'sale_id': int(sale['sell_id'])}
                    else:
                        if isinstance(id_sale_history[sale_str_date], dict):
                            id_sale_history[sale_str_date] = [id_sale_history[sale_str_date]] + [{'sale_price': float(sale['sell_price']), 'amount': int(sale['amount_sold']), 'sale_id': int(sale['sell_id'])},]
                        elif isinstance(id_sale_history[sale_str_date], list):
                            id_sale_history[sale_str_date] += [{'sale_price': float(sale['sell_price']), 'amount': int(sale['amount_sold']), 'sale_id': int(sale['sell_id'])},]
                else:
                    continue
            else:
                continue
    else:
        for sale in sales:
            #FIX APPENT AND MAKE A DICT LIST IN DATE WHEN EXISTING
            if id == int(sale['id']):
                sale_date = to_ymd(sale['sell_date'])
                sale_str_date= sale['sell_date']
                if sale_date >= start_date and sale_date <= end_date :
                    if sale_str_date not in list(id_sale_history.keys()):
                        id_sale_history[sale_str_date] = {'sale_price': float(sale['sell_price']), 'amount': int(sale['amount_sold']), 'sale_id': int(sale['sell_id'])}
                    else:
                        if isinstance(id_sale_history[sale_str_date], dict):
                            id_sale_history[sale_str_date] = [id_sale_history[sale_str_date]] + [{'sale_price': float(sale['sell_price']), 'amount': int(sale['amount_sold']), 'sale_id': int(sale['sell_id'])},]
                        elif isinstance(id_sale_history[sale_str_date], list):
                            id_sale_history[sale_str_date] += [{'sale_price': float(sale['sell_price']), 'amount': int(sale['amount_sold']), 'sale_id': int(sale['sell_id'])},]
                else:
                    continue
            else:
                continue
    return id_sale_history

def id_price_history(id, start_date, end_date):
    id = id if isinstance(id, int) else int(id)
    id_price_history = {}
    prices = dict_list_csv('prices.csv')
    if start_date == end_date or start_date == 0:
        for price in prices:
            if id == int(price['id']):
                price_date = to_ymd(price['price_date'])
                price_str_date= price['price_date']
                if price_date <= end_date:
                    if price_str_date not in list(id_price_history.keys()):
                        id_price_history[price_str_date] = float(price['price'])
                    else:
                        if isinstance(id_price_history[price_str_date], float):
                            id_price_history[price_str_date] = [id_price_history[price_str_date]] + [float(price['price']),]
                        elif isinstance(id_price_history[price_str_date], list):
                            id_price_history[price_str_date] += [float(price['price']),]

                else:
                    continue
            else:
                continue
    else:
        for price in prices:
            if id == int(price['id']):
                price_date = to_ymd(price['price_date'])
                price_str_date= price['price_date']
                if price_date >= start_date and price_date <= end_date:
                    if price_str_date not in list(id_price_history.keys()):
                        id_price_history[price_str_date] = float(price['price'])
                    else:
                        if isinstance(id_price_history[price_str_date], float):
                            id_price_history[price_str_date] = [id_price_history[price_str_date]] + [float(price['price']),]
                        elif isinstance(id_price_history[price_str_date], list):
                            id_price_history[price_str_date] += [float(price['price']),]
                else:
                    continue
            else:
                continue
    return id_price_history

def id_compound_history(id, start_date, end_date):
    id = id if isinstance(id, int) else int(id)
    compound_history= []
    price_history= id_price_history(id,start_date,end_date)
    sale_history= id_sale_history(id, start_date, end_date)
    buy_history= id_buy_history(id, start_date, end_date)
    price_dates= [to_ymd(i) for i in list(price_history.keys())]
    sale_dates= [to_ymd(i) for i in list(sale_history.keys())]
    buy_dates = [to_ymd(i) for i in list(buy_history.keys())]
    all_dates= sorted([*set(price_dates + sale_dates + buy_dates)])#datetime.date obj
    tupled_ph= sorted(list(zip(price_dates,list(price_history.values())))) # date[0], price[1]
    tupled_sh= [] # date[0], sale_price[1], amount[2], sale_id[3]
    tupled_bh= [] # date[0], buy_price[1], amount[2]
    compound_history = []

    for x, ph_item in enumerate(tupled_ph):
        if isinstance(ph_item[1], list):
            y= 1
            for i in ph_item[1]:
                tupled_ph.insert(x+y, tuple([ph_item[0], i]))
                y+=1
            del tupled_ph[x]
        else:
            continue
    for k, v in sale_history.items():
        if isinstance(v, dict):  
            tupled_sh.append(tuple([k,v['sale_price'],v['amount'],v['sale_id']]))
        elif isinstance(v,list):
            for d in v:
                tupled_sh.append(tuple([k,d['sale_price'],d['amount'],d['sale_id']]))
    
    for k, v in buy_history.items():
        if isinstance(v, dict):  
            tupled_bh.append(tuple([k,v['price'],v['amount']]))
        elif isinstance(v,list):
            for d in v:
                tupled_bh.append(tuple([k,d['price'],d['amount']]))
    
    #'Date','Buy Price','Sale Price','Bought','Sold', 'Profit', 'sale_id'
    for date in all_dates:
        compound_history.append([date, 0, 0, 0, 0, 0, -1])

    for buy_tup in tupled_bh:
        # date[0], buy_price[1], amount[3]
        new_items = []
        for inner_list in compound_history:
            if from_ymd(inner_list[0]) == buy_tup[0]:
                if not inner_list[1] and not inner_list[3]:
                    inner_list[1] = buy_tup[1]
                    inner_list[3] = buy_tup[2]
                else:                   
                    if [inner_list[0], buy_tup[1], 0, buy_tup[2], 0, 0, -1] not in compound_history:
                        new_item = [inner_list[0], buy_tup[1], 0, buy_tup[2], 0, 0, -1]
                        if new_item not in new_items:
                            new_items.append(new_item)
        if new_items:
            for item in new_items:
                compound_history.append(item)
                new_items.remove(item)
    
    #Rare for there to be more than one purchase in an id but it might happen with external imports, new item is used to prevent infinite loop over compound history
    for price_tup in tupled_ph:
        # date[0], sale price[2]
        new_items = []
        for inner_list in compound_history:
            if inner_list[0] == price_tup[0]:
                if not inner_list[2]:
                    inner_list[2] = price_tup[1]
                
                elif inner_list[2] and not inner_list[2] == price_tup[1]:
                    new_item = [inner_list[0], 0, 0, 0, 0, 0, -1]
                    new_item[2] = price_tup[1]
                    if new_item not in new_items:
                        new_items.append(new_item)
        if new_items:
            for item in new_items:
                compound_history.append(item)
                new_items.remove(item)           

    

    for sale_tup in tupled_sh:
        # date[0], sale_price[2], amount_sold[4],sale_id[6]
        for inner_list in compound_history:
            if from_ymd(inner_list[0]) == sale_tup[0]:
                if not inner_list[4]:
                    if inner_list[2] == sale_tup[1]:
                        inner_list[4] = sale_tup[2]
                        inner_list[6] = sale_tup[3]
                    elif not inner_list[2]:
                        inner_list[2] = sale_tup[1]
                        inner_list[4] = sale_tup[2]
                        inner_list[6] = sale_tup[3]
    
    for sale_tup in tupled_sh:
        new_items = []
        for inner_list in compound_history:
        # date[0], sale_price[2], amount_sold[4],sale_id[6]
            if inner_list[4] and inner_list[2] == sale_tup[1] and not inner_list[6] == sale_tup[3]:
                new_item = [i for i in inner_list]
                new_item[4] = sale_tup[2]
                if new_item not in new_items:
                        new_items.append(new_item)
        if new_items:
            for item in new_items:
                compound_history.append(item)
                new_items.remove(item)
    compound_history = sorted(compound_history, key=lambda tup: (tup[0],-tup[1])) 
    return compound_history

def same_names(csv_file, from_headers): 
    #can return true or a list
    csv_headers = list(pd.read_csv(csv_file).columns)
    alternative = csv_headers[1:] if csv_file == 'bought.csv' else csv_headers

    if (sorted(csv_headers) == sorted(from_headers)
       or (alternative == sorted(from_headers))):
        return True
    elif (set(csv_headers).issubset(set(from_headers)) 
       or(set(alternative)).issubset(set(from_headers))):
            extras = list(set(from_headers).difference(csv_headers))
            if ('sell_price' in extras or 'price' in extras or 'sale_price' in extras) and csv_file == 'bought.csv': 
                #this can be added thanks to the buy function which would smoothe the import
                return True
            else:
                CONSOLE.print(f'The import will continue but only the colums \n{csv_headers} will be imported\n{extras} will be left out')
                return True
    else: #no full match so now we go to equivalences
        option = '\nid can be filled in with giberish if absent' if csv_file == 'bought.csv' else ''
        titles = []
        missing_i=[]
        for x, head in enumerate(csv_headers):
            if head in from_headers:
                titles.append(head)
            elif head in [y.lower().replace(' ', '_') for y in from_headers]: #if the headers were almost the same this will detect that
                for z, from_h in enumerate(from_headers):
                    if from_h.lower().replace(' ', '_') == head:
                        titles.append(from_headers[z])
                        break #this prevents the list from going out of order
                    else:
                        continue
            else:
                titles.append(' ') #keeps the spot for easier inserting of correct headers
                missing_i.append(x)
        remaining_from = [i for i in from_headers if i not in titles]
        remaining_csv = [csv_headers[i] for i in missing_i]
        if remaining_csv:
            dif_titles = input(f'From this list: {remaining_from}\nPlease insert the key/column name equivalents for \n{remaining_csv} \nseparated by a comma "," do not add spaces after or before the comma {option}: ')
            if dif_titles:
                dif_titles = dif_titles.split(',')
                for x,index in enumerate(missing_i):
                    titles[index] = dif_titles[x]
                for title in dif_titles:
                    not_valid_header = []
                    all_valid = True
                    if title in from_headers:
                        continue
                    else: 
                        all_valid = False
                        not_valid_header.append(title)
                if all_valid:
                    return titles
                else:
                    CONSOLE.print(f'The following titles given were not valid:\n{not_valid_header}')
                    choice_input = ('Do you wish to retry/cancel?:')
                    if choice_input == 'retry':
                        same_names(csv_file, from_headers)
                    elif choice_input == 'cancel':
                        CONSOLE.print('The import will now be canceled')
                        return False
                    else:
                        CONSOLE.print('No valid action was chosen, the import will now be canceled')
                        return False
            else: #no input was given
                CONSOLE.print('No answer was given, the import will be canceled')
                return False
        else:
            return titles

def add_col_floats(table, col):
    float_list = [float(cell) for cell in table.columns[col].cells]
    float_sum = sum(float_list)
    round_float = round(float_sum, 2)
    return str(round_float)

#------------------------------- REPORT SECTION -------------------------------#
def report_inventory(start_date, end_date, verbosity= 1):
    long_fields = ['ID','Product Name','Amount','Buy Date','Buy Price','Expiration Date', 'Sale Price', 'Sold', 'Remaining', 'Expired', 'Profit']
    long_color_list = ['bold white','cyan1','royal_blue1','indian_red1','deep_pink1','orange1','green_yellow','green3','dodger_blue1','dark_red', 'chartreuse3']
    fields = long_fields[:3] + long_fields[4:6] + long_fields[8:]
    color_list = long_color_list[:3] + long_color_list[4:6] + long_color_list[8:]
    #['ID', 'Product Name','Amount','Buy Price', 'Expiration', 'Remaining', 'Expired', 'Profit']
    short_fields = [long_fields[1]] + long_fields[8:]
    short_color_list = [long_color_list[1]] + long_color_list[8:]
    #['Product Name', 'Remaining', 'Expired', 'Profit']

    inventory_table= Table(title= 'Inventory report', box = box.SIMPLE_HEAVY)
    inventory_table.show_footer = True
    item_list = makelist('id', start_date, end_date)
    name_item_list = makelist('name', start_date, end_date)
    

    total_remaining= 0
    total_bought= 0
    total_spent = 0
    total_sold = 0
    total_profit = 0

    if verbosity == 2:
        for x, field in enumerate(long_fields):
            inventory_table.add_column(field, style=long_color_list[x])
        for item in item_list:
            inventory_table.add_row(
                str(item.id), item.name, str(item.amount), str(item.buy_date), str(item.buy_price), str(item.expiration), str(item.sale_price), str(item.sold), str(item.remaining), (Text('Expired', style= 'red') if item.expired else Text('Valid', style = 'green')), str(item.profit)
                )
            total_spent += (item.amount * item.buy_price)
        inventory_table.columns[2].footer = str(sum([int(cell) for cell in inventory_table.columns[2].cells]))
        inventory_table.columns[4].footer = str(round(total_spent, 2))
        inventory_table.columns[7].footer = str(sum([int(cell) for cell in inventory_table.columns[7].cells]))
        inventory_table.columns[8].footer = str(sum([int(cell) for cell in inventory_table.columns[8].cells]))
        inventory_table.columns[10].footer = add_col_floats(inventory_table, 10)

    elif verbosity == 0:
        for x, field in enumerate(short_fields):
            inventory_table.add_column(field, style=short_color_list[x])
        for name_item in name_item_list:
            if name_item.remaining:
                inventory_table.add_row(
                    name_item.name, 
                    str(name_item.remaining),
                    (Text('Expired', style= 'red') if name_item.expired else Text('Valid', style = 'green')), 
                    str(round(name_item.profit, 2))
                    )
            else:
                continue
        inventory_table.columns[1].footer = str(sum([int(cell) for cell in inventory_table.columns[1].cells]))
        inventory_table.columns[3].footer = add_col_floats(inventory_table, 3)   

    else:
        for x, field in enumerate(fields):
            inventory_table.add_column(field, style=color_list[x])
        for item in item_list:
            if item.remaining:
                inventory_table.add_row(
                    str(item.id), item.name, str(item.amount), str(item.buy_price), str(item.expiration), str(item.remaining), (Text('Expired', style= 'red') if item.expired else Text('Valid', style = 'green')), str(item.profit)
                    )
                total_bought += item.amount
                total_remaining += item.remaining
                total_spent += (item.amount * item.buy_price)
                total_profit += item.profit
                total_sold += item.sold
            else:
                continue
        inventory_table.columns[2].footer = str(sum([int(cell) for cell in inventory_table.columns[2].cells]))
        inventory_table.columns[3].footer = str(round(total_spent, 2))
        inventory_table.columns[5].footer = str(sum([int(cell) for cell in inventory_table.columns[5].cells]))
        inventory_table.columns[7].footer = add_col_floats(inventory_table, 7)
    
    return inventory_table
            
def report_expired(start_date, end_date, verbosity= 1):
    long_fields = ['ID','Product Name','Amount','Buy Date','Buy Price','Expiration Date', 'Sale Price', 'Sold', 'Remaining', 'Expired', 'Profit']
    long_color_list = ['bold white','cyan1','royal_blue1','indian_red1','deep_pink1','orange1','green_yellow','green3','dodger_blue1','dark_red', 'chartreuse3']
    fields = long_fields[:3] + long_fields[4:6] + long_fields[8:]
    color_list = long_color_list[:3] + long_color_list[4:6] + long_color_list[8:]
    #['ID', 'Product Name','Amount','Buy Price', 'Expiration', 'Remaining', 'Expired', 'Profit']
    short_fields = [long_fields[1]] + long_fields[8:]
    short_color_list = [long_color_list[1]] + long_color_list[8:]
    #['Product Name', 'Remaining', 'Expired', 'Profit']

    expired_table= Table(title= 'Expired report', box = box.SIMPLE_HEAVY)
    expired_table.show_footer = True
    expired_table.footer_style = 'bold magenta'
    item_list = makelist('id', start_date, end_date)
    name_item_list = makelist('name', start_date, end_date)
    
    total_expired= 0
    total_bought= 0
    total_spent = 0
    total_sold = 0
    total_profit = 0
    i= 0

    if verbosity == 2:
        for field in long_fields:
            expired_table.add_column(field, style=long_color_list[i])
            i += 1
        for item in item_list:
            if item.expired:
                expired_table.add_row(
                    str(item.id), item.name, str(item.amount), str(item.buy_date), str(item.buy_price), str(item.expiration), str(item.sale_price), str(item.sold), str(item.remaining), (Text('Expired', style= 'red') if item.expired else Text('Valid', style = 'green')), str(item.profit)
                    )
                total_bought = total_bought + item.amount
                total_expired = total_expired + item.remaining
                total_spent = total_spent + (item.amount * item.buy_price)
                total_profit = total_profit + item.profit
                total_sold = total_sold + item.sold

        expired_table.columns[2].footer = str(total_bought)
        expired_table.columns[4].footer = str(round(total_spent, 2))
        expired_table.columns[7].footer = str(total_sold)
        expired_table.columns[8].footer = str(total_expired)
        expired_table.columns[10].footer = str(round(total_profit, 2))
        return expired_table

    elif verbosity == 0:
        for field in short_fields:
            expired_table.add_column(field, style=short_color_list[i])
            i += 1
        for name_item in name_item_list:
            if name_item.expired:
                expired_table.add_row(
                    name_item.name, 
                    str(name_item.remaining),
                    (Text('Expired', style= 'red') if name_item.expired else Text('Valid', style = 'green')), 
                    str(name_item.profit)
                    )
                total_expired = total_expired + name_item.remaining
                total_profit = total_profit + name_item.profit

            expired_table.columns[1].footer = str(total_expired)
            expired_table.columns[3].footer = str(round(total_profit, 2))
        return expired_table
    else:
        for field in fields:
            expired_table.add_column(field, style=color_list[i])
            i += 1
        for item in item_list:
            if item.expired:
                expired_table.add_row(
                    str(item.id), item.name, str(item.amount), str(item.buy_price), str(item.expiration), str(item.remaining), (Text('Expired', style= 'red') if item.expired else Text('Valid', style = 'green')), str(item.profit)
                    )
                total_bought = total_bought + item.amount
                total_expired = total_expired + item.remaining
                total_spent = total_spent + (item.amount * item.buy_price)
                total_profit = total_profit + item.profit
                total_sold = total_sold + item.sold

            expired_table.columns[2].footer = str(total_bought)
            expired_table.columns[3].footer = str(round(total_spent, 2))
            expired_table.columns[5].footer = str(total_expired)
            expired_table.columns[7].footer = str(round(total_profit,2))
        return expired_table

def report_profit(start_date, end_date, verbosity= 1):
    start_date = start_date if not start_date == 0 else end_date

    if start_date == end_date:
        date_message = from_ymd(end_date)
    else:
        date_message = (f'the period from {from_ymd(start_date)} to {from_ymd(end_date)}')
    
    sold = dict_list_csv('sold.csv')
    bought = dict_list_csv('bought.csv')
    colors = ['bold white','royal_blue1','purple' , 'dodger_blue1', 'dark_red', 'green3', 'green_yellow',  'chartreuse3']
    columns = ['Date','Item', 'Bought','Sold', 'Cost','Revenue', 'Profit','Percentage']
    profit_table = Table(title= f'Profit report for {date_message}:', box = box.SIMPLE_HEAVY)
    profit_table.show_footer = True

    bought_on_range = []
    for i in bought:
        if to_ymd(i['buy_date']) >= start_date and to_ymd(i['buy_date']) <= end_date:
            bought_on_range.append(i)
        else:
            pass

    sold_on_range = []
    for i in sold:
        if to_ymd(i['sell_date']) >= start_date and to_ymd(i['sell_date']) <= end_date:
            sold_on_range.append(i)
    
    sale_dates = [to_ymd(i['sell_date']) for i in sold_on_range]
    buy_dates = [to_ymd(i['buy_date']) for i in bought_on_range]
    all_dates = sorted([*set(sale_dates + buy_dates)])
    sale_ids = [int(i['id']) for i in sold_on_range]
    buy_ids = [int(i['id']) for i in bought_on_range]
    all_ids = sorted([*set(sale_ids + buy_ids)])
    all_names= [*set(get_name(id) for id in all_ids)]

    
    total_profit = 0
    for id in all_ids:
        total_profit += get_total_profit(id, end_date, start_date)
    
    total_profit = round(total_profit, 2)


    def bought(name):
        bought = 0
        for id in get_id_list(name):
            for b in bought_on_range:
                if int(b['id']) == id:
                    bought += int(b['amount'])
        return bought
        
    def profit(name):
        profit = 0
        for id in get_id_list(name):
            profit += get_total_profit(id, end_date, start_date)
        return round(profit,2)
    def amount(name):
        amount = 0
        for id in get_id_list(name):
            amount += amount_sold(id, end_date, start_date)
        return amount

    def cost(name):
        cost = 0
        for id in get_id_list(name):
            cost += get_total_cost(id, end_date, start_date)
        return round(cost,2)
    def revenue(name):
        revenue = 0
        for id in get_id_list(name):
            revenue += get_total_revenue(id, end_date, start_date)
        return round(revenue,2)

    if verbosity == 0:
        profit_message = (f'The total profit for {date_message} is: {total_profit}')
        return profit_message

    elif verbosity == 2:
        if start_date == end_date: 
            for x,n in enumerate(columns[1:]):
                profit_table.add_column(n, style = colors[x+1])
       
            for name in all_names:
                profit_table.add_row(name, str(bought(name)), str(amount(name)), str(cost(name)), str(revenue(name)),str(round(profit(name),2)), str(round((profit(name)/total_profit) * 100,2)) + ' %')
            profit_table.columns[1].footer = str(sum([int(cell) for cell in profit_table.columns[1].cells]))
            profit_table.columns[2].footer = str(sum([int(cell) for cell in profit_table.columns[2].cells]))
            profit_table.columns[3].footer = add_col_floats(profit_table, 3)
            profit_table.columns[4].footer = add_col_floats(profit_table, 4)
            profit_table.columns[5].footer = str(round(total_profit,2))
            profit_table.columns[6].footer = str(round(sum([float(cell.split()[0]) for cell in profit_table.columns[6].cells]))) + ' %'
            return profit_table
 
        else: #if not start_date == end_date
            #['Date','Item', 'Bought','Sold', 'Cost','Revenue', 'Profit','Percentage']
            
            for x,n in enumerate(columns):
                profit_table.add_column(n, style = colors[x])
            for s_date in all_dates:
                p_table = report_profit(s_date, s_date, verbosity)
                items = [cell for cell in p_table.columns[0].cells]
                bought = [cell for cell in p_table.columns[1].cells]
                sold = [cell for cell in p_table.columns[2].cells]
                costs = [cell for cell in p_table.columns[3].cells]
                revenues = [cell for cell in p_table.columns[4].cells]
                profits = [cell for cell in p_table.columns[5].cells]
                #for x, i in enumerate(costs):
                #    profits.append(float(revenues[x]) - float(i))
               # profits = [cell for cell in p_table.columns[4].cells]
                for x, i in enumerate(items):
                    profit_table.add_row(from_ymd(s_date),i, bought[x], sold[x], costs[x], revenues[x], profits[x], str(round((float(profits[x])/total_profit) * 100,2)) + ' %')
            profit_table.columns[2].footer = str(sum([int(cell) for cell in profit_table.columns[2].cells]))
            profit_table.columns[3].footer = str(sum([int(cell) for cell in profit_table.columns[3].cells]))
            profit_table.columns[4].footer = add_col_floats(profit_table, 4)
            profit_table.columns[5].footer = add_col_floats(profit_table, 5)
            profit_table.columns[6].footer = add_col_floats(profit_table, 6)
            profit_table.columns[7].footer = str(round(sum([float(cell.split()[0]) for cell in profit_table.columns[7].cells]))) + ' %'
             
            return profit_table

    else: #if verbosity = 1
        short_cols = columns[1:4] + columns [6:] 
        # 'Item', 'Bougt', 'Sold' 'Profit', 'Percentage'
        short_colors = colors[1:4] + colors[6:]
        if start_date == end_date:
            for x,n in enumerate(short_cols):
                profit_table.add_column(n, style = short_colors[x])
            
            p_table = report_profit(start_date, end_date, verbosity = 2) 
            items = [cell for cell in p_table.columns[0].cells]
            bought = [cell for cell in p_table.columns[1].cells]
            sold = [cell for cell in p_table.columns[2].cells]
            profits = [cell for cell in p_table.columns[5].cells]
            percentages = [cell for cell in p_table.columns[6].cells]
            for x, i in enumerate(items):
                profit_table.add_row(i, bought[x], sold[x], profits[x], percentages[x])
            
            profit_table.columns[1].footer = str(sum([int(cell) for cell in profit_table.columns[1].cells]))
            profit_table.columns[2].footer = str(sum([int(cell) for cell in profit_table.columns[2].cells]))
            profit_table.columns[3].footer = add_col_floats(profit_table, 3)
            profit_table.columns[4].footer = str(round(sum([float(cell.split()[0]) for cell in profit_table.columns[4].cells]))) + ' %'

            return profit_table

        else: #if not start_date == end_date
            for x,n in enumerate(['Date'] + short_cols[1:]):
                    # 'Date', 'Bougt', 'Sold' 'Profit', 'Percentage'
                profit_table.add_column(n, style = short_colors[x])

            v2_p_table = {}
            p_table = report_profit(start_date, end_date, verbosity = 2)
            dates = [cell for cell in p_table.columns[0].cells]
            items = [cell for cell in p_table.columns[1].cells]
            bought = [cell for cell in p_table.columns[2].cells]
            sold = [cell for cell in p_table.columns[3].cells]
            profits = [cell for cell in p_table.columns[6].cells]
            percentages = [cell for cell in p_table.columns[7].cells]
            for x, i in enumerate(dates):
                if i not in v2_p_table:
                    v2_p_table[i] = {'bought': int(bought[x]), 'sold': int(sold[x]), 'profits' : float(profits[x]), 'percentages' : float(percentages[x].split()[0]) }
                elif i in v2_p_table:
                    v2_p_table[i]['bought'] += int(bought[x])
                    v2_p_table[i]['sold'] += int(sold[x])
                    v2_p_table[i]['profits'] += float(profits[x])
                    v2_p_table[i]['percentages'] += float(percentages[x].split()[0])
            
            for x, dict in enumerate(v2_p_table):
                profit_table.add_row(str(dict), str(v2_p_table[dict]['bought']),str(v2_p_table[dict]['sold']), str(round(v2_p_table[dict]['profits'],2)), str(round(v2_p_table[dict]['percentages'],2)))
            
            profit_table.columns[1].footer = str(sum([int(cell) for cell in profit_table.columns[1].cells]))
            profit_table.columns[2].footer = str(sum([int(cell) for cell in profit_table.columns[2].cells]))
            profit_table.columns[3].footer = add_col_floats(profit_table, 3)
            profit_table.columns[4].footer = str(round(sum([float(cell.split()[0]) for cell in profit_table.columns[4].cells]))) + ' %'

            return profit_table

def report_revenue(start_date, end_date, verbosity):
    start_date = start_date if not start_date == 0 else end_date

    if start_date == end_date:
        date_message = from_ymd(end_date)
    else:
        date_message = (f'the period from {from_ymd(start_date)} to {from_ymd(end_date)}')

    revenue_table = Table(title= f'Revenue report for {date_message}:', box = box.SIMPLE_HEAVY)
    revenue_table.show_footer = True
    sold = dict_list_csv('sold.csv')
    colors = ['bold white','royal_blue1', 'green3', 'dark_red', 'green_yellow', 'chartreuse3']
    columns = ['Date','Item', 'Amount', 'Cost','Revenue', 'Percentage']
    revenue_message = False

    def amount(name):
        amount = 0
        for id in get_id_list(name):
            amount += amount_sold(id, end_date, start_date)
        return amount
    def cost(name):
        cost = 0
        for id in get_id_list(name):
            cost += get_total_cost(id, end_date, start_date)
        return cost
    def revenue(name):
        revenue = 0
        for id in get_id_list(name):
            revenue += get_total_revenue(id, end_date, start_date)
        return revenue


    if verbosity == 2:
        if end_date == start_date:
            sold_on_date =[i for i in sold if to_ymd(i['sell_date'])==end_date]
            sold_items = [*set(get_name(int(i['id'])) for i in sold_on_date)]

            all_revenue = sum([revenue(name) for name in sold_items])
            for x,n in enumerate(columns[1:]):
                revenue_table.add_column(n, style = colors[x+1])

            for name in sold_items:
                # ['Date','Item', 'Amount', 'Cost','Revenue', 'Percentage']

                revenue_table.add_row(name, str(amount(name)), str(cost(name)), str(revenue(name)), str(round((revenue(name)/all_revenue) * 100,2)) + ' %')
            revenue_table.columns[1].footer = str(sum([int(cell) for cell in revenue_table.columns[1].cells]))
            revenue_table.columns[2].footer = add_col_floats(revenue_table, 2)
            revenue_table.columns[3].footer = add_col_floats(revenue_table, 3)
            percent_sum = round(sum([float(cell.split()[0]) for cell in revenue_table.columns[4].cells]))
            revenue_table.columns[4].footer = ('100' if percent_sum >= 100 and percent_sum <= 101 else str(percent_sum)) + ' %'
            return revenue_table
        else: #if not start_date == end_date
            sold_on_range = []
            for i in sold:
                if to_ymd(i['sell_date']) >= start_date and to_ymd(i['sell_date']) <= end_date:
                    sold_on_range.append(i)
            sold_items = [*set(get_name(int(i['id'])) for i in sold_on_range)]
            sale_dates = [*set(to_ymd(i['sell_date']) for i in sold_on_range)]
            all_revenue = sum([revenue(name) for name in sold_items])

            for x,n in enumerate(columns):
                revenue_table.add_column(n, style = colors[x])
            for s_date in sale_dates:
                r_table = report_revenue(s_date, s_date, verbosity)
                items = [cell for cell in r_table.columns[0].cells]
                amounts = [cell for cell in r_table.columns[1].cells]
                costs = [cell for cell in r_table.columns[2].cells]
                revenues = [cell for cell in r_table.columns[3].cells]
                for x, i in enumerate(items):
                 revenue_table.add_row(from_ymd(s_date),i, amounts[x], costs[x], revenues[x], str(round((float(revenues[x])/all_revenue) * 100,2)) + ' %')
            revenue_table.columns[2].footer = str(sum([int(cell) for cell in revenue_table.columns[2].cells]))
            revenue_table.columns[3].footer = add_col_floats(revenue_table, 3)
            revenue_table.columns[4].footer = add_col_floats(revenue_table, 4)
            percent_sum = round(sum([float(cell.split()[0]) for cell in revenue_table.columns[5].cells]))
            revenue_table.columns[5].footer = ('100' if percent_sum >= 100 and percent_sum <= 101 else str(percent_sum)) + ' %'
            return revenue_table

    elif verbosity == 0:
        ids = [*set(i['id'] for i in sold) ]
        total_revenue = 0
        for id in ids:
            total_revenue += get_total_revenue(id, end_date, start_date)
        
        revenue_message = (f'The total revenue for {date_message} is: {total_revenue}')
        return revenue_message
    else: #if verbosity = 1
        short_cols = columns[:3] + columns [4:] 
        # 'Date','Item', 'amount' 'Revenue', 'Percentage'
        short_colors = colors[:3] + colors[4:]
        if start_date == end_date:
            for x,n in enumerate(short_cols[1:]):
                revenue_table.add_column(n, style = short_colors[x+1])
            
            r_table = report_revenue(start_date, end_date, verbosity = 2) 
            items = [cell for cell in r_table.columns[0].cells]
            amounts = [cell for cell in r_table.columns[1].cells]
            revenues = [cell for cell in r_table.columns[3].cells]
            percentages = [cell for cell in r_table.columns[4].cells]
            for x, i in enumerate(items):
                revenue_table.add_row(i, amounts[x], revenues[x], percentages[x])
            
            revenue_table.columns[1].footer = str(sum([int(cell) for cell in revenue_table.columns[1].cells]))
            revenue_table.columns[2].footer = add_col_floats(revenue_table, 2)
            percent_sum = round(sum([float(cell.split()[0]) for cell in revenue_table.columns[3].cells]))
            revenue_table.columns[3].footer = ('100' if percent_sum >= 100 and percent_sum <= 101 else str(percent_sum)) + ' %'
            return revenue_table

        else: #if not start_date == end_date
            for x,n in enumerate(short_cols):
                revenue_table.add_column(n, style = short_colors[x])
            r_table = report_revenue(start_date, end_date, verbosity = 2)
            dates = [cell for cell in r_table.columns[0].cells]
            items = [cell for cell in r_table.columns[1].cells]
            amounts = [cell for cell in r_table.columns[2].cells]
            revenues = [cell for cell in r_table.columns[4].cells]
            percentages = [cell for cell in r_table.columns[5].cells]
            for x, i in enumerate(items):
                revenue_table.add_row(dates[x], i, amounts[x], revenues[x], percentages[x])
            
            revenue_table.columns[2].footer = str(sum([int(cell) for cell in revenue_table.columns[2].cells]))
            revenue_table.columns[3].footer = add_col_floats(revenue_table, 3)
            percent_sum = round(sum([float(cell.split()[0]) for cell in revenue_table.columns[4].cells]))
            revenue_table.columns[4].footer = ('100' if percent_sum >= 99 and percent_sum <= 101 else str(percent_sum)) + ' %'

            return revenue_table

def report_item(start_date, end_date, verbosity= 1,item= 0, id= 0 ):

    long_fields = ['Date','Buy Price','Sale Price','Bought','Sold', 'Profit']
    long_color_list = ['indian_red1','deep_pink1','green_yellow','dodger_blue1','green3', 'chartreuse3']
    short_fields = long_fields[1:]
    short_color_list = long_color_list[1:]
    #['Price','Bought','Sold', 'Profit']
    i = 0
    bp = 0
    item_table= Table(title= f'{item if item else get_name(id)} report' + (f' with id: {id}' if id else ''), box = box.SIMPLE_HEAVY)
    item_table.show_footer = True

    if item:
        if verbosity == 2:
            totals_table = Table(title= 'Totals')
            buy_prices =[]
            sale_prices =[]
            total_bought = 0
            total_sold = 0
            total_profit = 0
            ids = get_id_list(item)
            for id in ids:
                id_table = report_item(start_date, end_date, verbosity, id= id)
                item_table.add_row(id_table)
                buy_prices.append(float(id_table.columns[1].footer))
                sale_prices.append(float(id_table.columns[2].footer))
                total_bought += int(id_table.columns[3].footer)
                total_sold += int(id_table.columns[4].footer)
                total_profit += float(id_table.columns[5].footer)
            for y, x in enumerate(long_fields):
                totals_table.add_column(x, style= long_color_list[y])
            totals_table.add_row(
                '',str(round(sum(buy_prices)/len(buy_prices), 2)),
                str(round(sum(sale_prices)/len(sale_prices), 2)), 
                str(total_bought), str(total_sold), 
                str(round(total_profit,2)))
            item_table.add_row(totals_table)
            item_table.show_footer = False                
            return item_table
            

        else:
            item_compound_history = [] 
            ids = get_id_list(item)
            for id in ids:
                item_compound_history += id_compound_history(id, start_date, end_date)
            item_compound_history = sorted(item_compound_history, key=lambda tup: (tup[0],-tup[1]))
            buy_prices = [*set(i[1] for i in item_compound_history if i[1])]
            sell_prices = [*set(i[2] for i in item_compound_history if i[2])]
            bought = 0
            sold = 0
            profit_total = 0
            compact_history = []
            for hist_item in item_compound_history:
                if compact_history:
                    if hist_item[:3] not in [c[:3] for c in compact_history]:
                        compact_history.append(hist_item[:3]+[0,0,0])
                else:
                    compact_history.append(hist_item[:3]+[0,0,0])
            for hist_item in item_compound_history:
                    for c_item in compact_history:
                        if hist_item[:3] == c_item[:3]:
                            c_item[3] += hist_item[3]
                            c_item[4] += hist_item[4]
            
            if verbosity == 0:
                mini_history = []
                for c_item in compact_history:
                    if mini_history:
                        if c_item[1:3] not in [m[:2] for m in mini_history]:
                            mini_history.append(c_item[1:3]+[0,0,0])
                    else:
                        mini_history.append(c_item[1:3]+[0,0,0])
                for c_item in compact_history:
                    for m_item in mini_history:
                        if c_item[1:3] == m_item[:2]:
                            m_item[2] += c_item[3]
                            m_item[3] += c_item[4]

                for x, field in enumerate(short_fields):
                    item_table.add_column(field, style=short_color_list[x])

                for i in mini_history:
                    bp = i[0] if i[0] else bp
                    profit = (i[3]*i[1])-(bp*(i[2] if i[2] else i[3]))
                    item_table.add_row(
                        str(i[0]) if i[0] else '-',
                        str(i[1]) if i[1] else '-',
                        str(i[2]) if i[2] else '-',
                        str(i[3]) if i[3] else '-',
                        str(round(profit, 2)) if profit else '-')

                    bought += i[3]
                    sold += i[4]
                    profit_total += profit
                item_table.columns[0].footer = str(round(sum(buy_prices)/len(buy_prices),2))
                item_table.columns[1].footer = str(round(sum(sell_prices)/len(sell_prices),2))
                item_table.columns[2].footer = str(bought)
                item_table.columns[3].footer = str(sold)
                item_table.columns[4].footer = str(round(profit_total, 2))
                return item_table

            else: #if verbosity 1
                for x, field in enumerate(long_fields):
                    item_table.add_column(field, style=long_color_list[x])

                for i in compact_history:
                    bp = i[1] if i[1] else bp
                    profit = (i[4]*i[2])-(bp*(i[3] if i[3] else i[4]))
                    item_table.add_row(from_ymd(i[0]),
                        str(i[1]) if i[1] else '-',
                        str(i[2]) if i[2] else '-',
                        str(i[3]) if i[3] else '-',
                        str(i[4]) if i[4] else '-',
                        str(round(profit, 2)) if profit else '-')

                    bought += i[3]
                    sold += i[4]
                    profit_total += profit
                item_table.columns[1].footer = str(round(sum(buy_prices)/len(buy_prices),2))
                item_table.columns[2].footer = str(round(sum(sell_prices)/len(sell_prices),2))
                item_table.columns[3].footer = str(bought)
                item_table.columns[4].footer = str(sold)
                item_table.columns[5].footer = str(round(profit_total, 2))
                return item_table

    elif id:
        compound_history = id_compound_history(id, start_date,end_date)
        buy_prices = [*set(i[1] for i in compound_history if i[1])]
        sell_prices = [*set(i[2] for i in compound_history if i[2])]
        bought = 0
        sold = 0
        profit_total = 0

    #price hit {'date': price, 'date': price}
    #sale hit {'date': {'sale_price': price, 'amount': amount_sold},
    #          'date': {'sale_price': price, 'amount': amount_sold}}
    #buy hit {'date':{'price': buy price, 'amount': amount},
    #         'date':{'price': buy price, 'amount': amount},}
        if verbosity == 2:
            for x, field in enumerate(long_fields):
                item_table.add_column(field, style=long_color_list[x])
            for i in compound_history:
                bp = i[1] if i[1] else bp
                profit = (i[4]*i[2])-(bp*(i[3] if i[3] else i[4]))
                item_table.add_row(
                    from_ymd(i[0]),
                    str(i[1]) if i[1] else '-',
                    str(i[2]) if i[2] else '-',
                    str(i[3]) if i[3] else '-',
                    str(i[4]) if i[4] else '-',
                    str(round(profit, 2)) if profit else '-'
                    )
                bought += i[3]
                sold += i[4]
                profit_total += profit
            item_table.columns[1].footer = str(round(sum(buy_prices)/len(buy_prices),2))
            item_table.columns[2].footer = str(round(sum(sell_prices)/len(sell_prices),2))
            item_table.columns[3].footer = str(bought)
            item_table.columns[4].footer = str(sold)
            item_table.columns[5].footer = str(round(profit_total, 2))
            return item_table

        else:
            compact_history = []
            for hist_item in compound_history:
                if compact_history:
                    if hist_item[:3] not in [c[:3] for c in compact_history]:
                        compact_history.append(hist_item[:3]+[0,0,0])
                else:
                    compact_history.append(hist_item[:3]+[0,0,0])

            for hist_item in compound_history:
                    for c_item in compact_history:
                        if hist_item[:3] == c_item[:3]:
                            c_item[3] += hist_item[3]
                            c_item[4] += hist_item[4]

            if verbosity == 0:
                mini_history = []

                for c_item in compact_history:
                    if mini_history:
                        if c_item[1:3] not in [m[:2] for m in mini_history]:
                            mini_history.append(c_item[1:3]+[0,0,0])
                    else:
                        mini_history.append(c_item[1:3]+[0,0,0])

                for c_item in compact_history:
                    for m_item in mini_history:
                        if c_item[1:3] == m_item[:2]:
                            m_item[2] += c_item[3]
                            m_item[3] += c_item[4]

                for x, field in enumerate(short_fields):
                    item_table.add_column(field, style=short_color_list[x])

                for i in mini_history:
                    bp = i[0] if i[0] else bp
                    profit = (i[3]*i[1])-(bp*(i[2] if i[2] else i[3]))
                    
                    item_table.add_row(
                        str(i[0]) if i[0] else '-',
                        str(i[1]) if i[1] else '-',
                        str(i[2]) if i[2] else '-',
                        str(i[3]) if i[3] else '-',
                        str(round(profit, 2)) if profit else '-')
                    bought += i[3]
                    sold += i[4]
                    profit_total += profit
                item_table.columns[0].footer = str(round(sum(buy_prices)/len(buy_prices),2))
                item_table.columns[1].footer = str(round(sum(sell_prices)/len(sell_prices),2))
                item_table.columns[2].footer = str(bought)
                item_table.columns[3].footer = str(sold)
                item_table.columns[4].footer = str(round(profit_total, 2))
                return item_table

            else:

                for x, field in enumerate(long_fields):
                    item_table.add_column(field, style=long_color_list[x])

                for i in compact_history:
                    bp = i[1] if i[1] else bp
                    profit = (i[4]*i[2])-(bp*(i[3] if i[3] else i[4]))
                    item_table.add_row(from_ymd(i[0]),
                        str(i[1]) if i[1] else '-',
                        str(i[2]) if i[2] else '-',
                        str(i[3]) if i[3] else '-',
                        str(i[4]) if i[4] else '-',
                        str(round(profit, 2)) if profit else '-')

                    bought += i[3]
                    sold += i[4]
                    profit_total += profit
                item_table.columns[1].footer = str(round(sum(buy_prices)/len(buy_prices),2))
                item_table.columns[2].footer = str(round(sum(sell_prices)/len(sell_prices),2))
                item_table.columns[3].footer = str(bought)
                item_table.columns[4].footer = str(sold)
                item_table.columns[5].footer = str(round(profit_total, 2))
                return item_table

 
#----------------------------- BUY ACTION HANDLING ----------------------------#
def buy(product_name, amount, buy_date, buy_price, expiration_date, id= 0, sell_price = 0):
    #revise similar prices for items of the same name and ask if the same price is desired
    id = (get_last_id("bought.csv") +1) if not id else id
    with open('bought.csv', 'a', newline='') as buying_file:
        field_names = ['id', 'amount', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
        writer = csv.DictWriter(buying_file, fieldnames=field_names)
        writer.writerow({'id': id, 'amount': amount, 'product_name': product_name, 'buy_date': buy_date, 'buy_price': buy_price, 'expiration_date': expiration_date})
    with open('prices.csv', 'a', newline='') as price_history_file:
        field_names_b = ['id', 'price', 'price_date']
        writer_b = csv.DictWriter(price_history_file, fieldnames=field_names_b)
        if sell_price:
            writer_b.writerow({'id': id, 'price': sell_price, 'price_date': buy_date})
        else:
            ids = get_id_list(product_name)
            if ids:
                price_ids = [int(i['id']) for i in dict_list_csv('prices.csv') if float(i['price'])]
                price_ids = [i for i in price_ids if i in ids]
                if price_ids:
                    last_price = last_sale_price(max(price_ids, default= 0),buy_date)
                else:
                    last_price = 0
            else:
                last_price = 0
            sell_price = last_price if last_price else 0
            writer_b.writerow({'id': id, 'price': sell_price, 'price_date': buy_date})


#--------------------------- PRICE SETTING HANDLING ---------------------------#
def set_price(price, price_date, list = None, id = 0, item = ''):
    if id:
        if last_sale_price(id,price_date) == price:
            pass
        else:
            with open('prices.csv', 'a', newline='') as price_file:
                field_names = ['id','price','price_date']
                writer = csv.DictWriter(price_file, fieldnames=field_names)
                writer.writerow({'id': id, 'price':price, 'price_date':price_date})
            CONSOLE.print(f'The price for id {id} has been set to {price}')
    elif item:
        item = item
        id_list= get_id_list(item)
        set_price(price, price_date, list = id_list)
    #if it is an item, ite recourses to the list method
    elif list:
        for i in range(len(list)):
            if last_sale_price(id,price_date) == price:
               pass
            else:
                with open('prices.csv', 'a', newline='') as price_file:
                    field_names = ['id','price','price_date']
                    writer = csv.DictWriter(price_file, fieldnames=field_names)
                    writer.writerow({'id': list[i], 'price':price, 'price_date':price_date})
                CONSOLE.print(f'The price for id {list[i]} has been set to {price}')
        

#---------------------------- SELL ACTION HANDLING ----------------------------#
def sell(sell_date, sold_amount = 1, sell_price = None, id= 0, item= 0):
    last_sale = get_last_id('sold.csv')
    if id:
        item_id = get_available(sell_date, sold_amount, id=id) #can return False, an int or a list of tuples 
        if type(item_id) == int:
            sell_id = (get_last_id('sold.csv') +1)
            if sell_price == None:
                sell_price = float(last_sale_price(id=item_id, given_date =sell_date))
                if sell_price == 0:
                    sell_price = float(input('The current price for this item is 0, please insert a price: '))
                    set_price(sell_price, sell_date, id= item_id)
            elif sell_price:
                product_name = get_name(item_id)
                name_matches = get_id_list(product_name)
                if len(name_matches) >1:
                    do_same = input(f'Should the same price be set for all {len(name_matches)} instances of {product_name}? \n    yes/no: ')
                    if do_same == 'yes':
                        set_price(sell_price, sell_date, list= name_matches)
                    elif do_same == 'no':
                        set_price(sell_price, sell_date, id= item_id)
                elif len(name_matches) == 1:
                    set_price(sell_price, sell_date, id= item_id[0])
            with open('sold.csv', 'a', newline='') as selling_file:
                field_names = ['sell_id', 'id', 'amount_sold', 'sell_date', 'sell_price']
                writer = csv.DictWriter(selling_file, fieldnames=field_names)
                writer.writerow({'sell_id': sell_id, 'id': item_id, 'amount_sold': sold_amount, 'sell_date': sell_date, 'sell_price': sell_price})
                sale_total = sold_amount*sell_price
            last_after_sale = get_last_id('sold.csv')
            if last_after_sale > last_sale:
                CONSOLE.print(f'Sale completed for {sale_total}')
        elif type(item_id) == list:
            for i in item_id:
                if type(i) == tuple:
                    #i[0] is the id i[1] is the amount
                    sell(sell_date,i[1],sell_price, id= i[0])
        
            
    elif item:
        item_id =get_available(date = sell_date,sold_amount = sold_amount,item= item) 
        if type(item_id) == int:
            sell_id = (get_last_id('sold.csv') +1)
            if sell_price == None:
                sell_price = float(last_sale_price(id=item_id, given_date =sell_date))
                if sell_price == 0:
                    sell_price = float(input('The current price for this item is 0, please insert a price: '))
                    set_price(sell_price, sell_date, id= item_id)
            elif sell_price:
                product_name = get_name(item_id)
                name_matches = get_id_list(product_name)
                if len(name_matches) >1:
                    do_same = input(f'Should the same price be set for all {len(name_matches)} instances of {product_name}? \n    yes/no: ')
                    if do_same == 'yes':
                        set_price(sell_price, sell_date, list= name_matches)
                    elif do_same == 'no':
                        set_price(sell_price, sell_date, id= item_id)
                else:#if it is a one item list
                    set_price(sell_price, sell_date, id= item_id[0])
            with open('sold.csv', 'a', newline='') as selling_file:
                field_names = ['sell_id', 'id', 'amount_sold', 'sell_date', 'sell_price']
                writer = csv.DictWriter(selling_file, fieldnames=field_names)
                writer.writerow({'sell_id': sell_id, 'id': item_id, 'amount_sold': sold_amount, 'sell_date': sell_date, 'sell_price': sell_price})
                sale_total = sold_amount*sell_price
            last_after_sale = get_last_id('sold.csv')
            if last_after_sale > last_sale:
                CONSOLE.print(f'Sale completed for {sale_total}')
        elif type(item_id) == list:
            for i in item_id:
                #Type check is there to maybe later implement being able to insert a list of ids to sell????
                if type(i) == tuple:
                    #i[0] is the id i[1] is the amount
                    sell(sell_date,i[1],sell_price, id= i[0])
    

#-------------------------- SAVE ACTION HANDLING ----------------------------#
def save(dest_type, table, sys_date):
    dict_list =[]
    if isinstance(table, str):
        t_dict_item = {}
        phrase = table.split()
        txt_0 = phrase[2]
        date_txt = [i for i in phrase if to_ymd(i)]
        if len(date_txt) > 1:
            title = txt_0 + '_' + date_txt[0] + '_to_' + date_txt[1]
            t_dict_item[title] = phrase[-1]
        else:
            title = txt_0 + '_' + date_txt[0]
            t_dict_item[title] = phrase[-1]
        saved_file = (txt_0 + '_report_' + from_ymd(sys_date) + '.' + dest_type)
        dict_list.append(t_dict_item)
    else:
        title = table.title.lower().replace(':', '').replace('with ', '')
        title = title.replace(' ', '_')
        saved_file = (title + '_' + from_ymd(sys_date) + '.' + dest_type)
        def make_dict(i_table):
            for x in range(i_table.row_count):
                i_dict = {}
                for column in i_table.columns:
                    d_value = list(column.cells)[x]
                    d_value = d_value if not isinstance(d_value, Text) else str(d_value)
                    i_dict[column.header] = d_value
                dict_list.append(i_dict)

        for x in range(table.row_count):
            dict_item = {}
            for column in table.columns:
                d_value = list(column.cells)[x]
                if isinstance(d_value, Table): #this handles the v2 item reports
                    make_dict(d_value)
                else:
                    d_value = d_value if not isinstance(d_value, Text) else str(d_value)
                    dict_item[column.header] = d_value
            
            dict_list.append(dict_item)
   
    saved_path =os.path.join('saved', saved_file)
    if dest_type == 'xlsx':
        df = pd.DataFrame(data=dict_list)
        df.to_excel(saved_path, index = False)
    elif dest_type == 'json':
        json_list = json.dumps(dict_list, indent= 2)
        with open(saved_path, 'w') as json_save:
            json_save.write(json_list)
    elif dest_type == 'csv':
        with open(saved_path, 'w') as csv_save:
            writer = csv.DictWriter(csv_save, fieldnames= dict_list[0].keys() )

            writer.writeheader()
            for row in dict_list:
                
                writer.writerow(row)
    return str(saved_path)

def export(csv_file, sys_date, dest_type, destination = False): #almost the same as save(), divided for clarity
    dict_list = dict_list_csv(csv_file)
    title = destination if destination else csv_file[:-4]
    saved_file = (title + '_' + from_ymd(sys_date) + '.' + dest_type)
    saved_path =os.path.join('saved', saved_file)
    
    dict_list = dict_list_csv(csv_file)

    if dest_type == 'xlsx':
        df = pd.DataFrame(data=dict_list)
        df.to_excel(saved_path, index = False)
    elif dest_type == 'json':
        json_list = json.dumps(dict_list, indent= 2)
        with open(saved_path, 'w') as json_save:
            json_save.write(json_list)
    elif dest_type == 'csv':
        with open(saved_path, 'w') as csv_save:
            writer = csv.DictWriter(csv_save, fieldnames= dict_list[0].keys() )
            writer.writeheader()
            for row in dict_list:
                
                writer.writerow(row)
    return str(saved_path)


#------------------------- CLASS LIST MAKERS -------------------------#
def makelist(version, start_date, end_date): #makes a list of dictionaries based on product name or id, focused on reporting the inventory
    id_item_list = []
    name_item_list = []
    bought_list = dict_list_csv('bought.csv')
    if version == 'id': #This will make a list of class instances based on the ID of the item
        for bought_item in bought_list:
            item_id = int(bought_item['id'])
            item_name = bought_item['product_name']
            item_amount = int(bought_item['amount'])
            item_buy_price = float(bought_item['buy_price'])
            item_buy_date = to_ymd(bought_item['buy_date'])
            item_expiration = to_ymd(bought_item['expiration_date'])
            item_sale_price = last_sale_price(item_id, end_date)
            item_sold = amount_sold(item_id, end_date)
            item_remaining = item_amount - item_sold
            item_expired = getdate.check_expired(item_expiration)
            item_profit = get_total_profit(item_id,end_date) #start date as well?
            if start_date == end_date or start_date == 0:
                if item_buy_date <= end_date:
                    id_item_list.append(
                        ItemById(id= item_id, name= item_name, amount= item_amount ,buy_price= item_buy_price, buy_date= item_buy_date, expiration= item_expiration, sale_price= item_sale_price, sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
            else:
                if item_buy_date >= start_date and item_buy_date <= end_date:
                    id_item_list.append(
                        ItemById(id= item_id, name= item_name, amount= item_amount ,buy_price= item_buy_price, buy_date= item_buy_date, expiration= item_expiration, sale_price= item_sale_price, sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
        return id_item_list          
    elif version == 'name': #This will create a list that merges information based on the item name, separated only by wether some are expired or not
        name_list = []
        expired_name_list = []
        for bought_item in bought_list:
            item_id = int(bought_item['id'])
            item_name = bought_item['product_name']
            item_amount = int(bought_item['amount'])
            item_buy_price = float(bought_item['buy_price'])
            item_buy_date = to_ymd(bought_item['buy_date'])
            item_expiration = to_ymd(bought_item['expiration_date'])
            item_sale_price = last_sale_price(item_id, end_date)
            item_sold = amount_sold(item_id, end_date)
            item_remaining = item_amount - item_sold
            item_expired = getdate.check_expired(item_expiration)
            item_profit = get_total_profit(item_id,end_date)
            if not item_remaining: 
                continue #fixes out of stock items getting added and messing up the profit calculations
            if start_date == end_date or (start_date == 0):
                if item_buy_date <= end_date:
                    if item_name in name_list and item_name not in expired_name_list and item_expired:
                        expired_name_list.append(item_name)
                        name_item_list.append(
                            ItemByName(name= item_name, amount= item_amount ,buy_price= [item_buy_price], buy_date= [item_buy_date], expiration= [item_expiration], sale_price= [item_sale_price], sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
                    elif item_name in name_list and not item_expired:
                        for class_item in name_item_list:
                            if class_item.name == item_name and class_item.expired == item_expired:
                                class_item.amount = class_item.amount + item_amount
                                #buy_price, buy date is list
                                #modify tojust give an average?
                                class_item.buy_price = make_classlist(class_item.buy_price, item_buy_price)
                                class_item.buy_date = make_classlist(class_item.buy_date, item_buy_date)
                                class_item.expiration = make_classlist(class_item.expiration, item_expiration)
                                class_item.sale_price = make_classlist(class_item.sale_price, item_sale_price)
                                class_item.sold = class_item.sold + item_sold
                                class_item.remaining = class_item.remaining if item_expired else class_item.remaining + item_remaining
                                class_item.profit = class_item.profit + item_profit
                    elif item_name not in name_list and item_name in expired_name_list and not item_expired:
                        name_list.append(item_name)
                        name_item_list.append(
                            ItemByName(name= item_name, amount= item_amount ,buy_price= [item_buy_price], buy_date= [item_buy_date], expiration= [item_expiration], sale_price= [item_sale_price], sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
                    elif item_name in expired_name_list:
                        for class_item in name_item_list:
                            if class_item.name == item_name and class_item.expired == item_expired:
                                class_item.amount = class_item.amount + item_amount
                                class_item.buy_price = make_classlist(class_item.buy_price, item_buy_price)
                                class_item.buy_date = make_classlist(class_item.buy_date, item_buy_date)
                                class_item.expiration = make_classlist(class_item.expiration, item_expiration)
                                class_item.sale_price = make_classlist(class_item.sale_price, item_sale_price)
                                class_item.sold = class_item.sold + item_sold
                                class_item.remaining = class_item.remaining + item_remaining
                                class_item.profit = class_item.profit + item_profit
                    else:
                        if item_expired:
                            expired_name_list.append(item_name)
                        elif not item_expired:
                            name_list.append(item_name)
                        name_item_list.append(
                            ItemByName(name= item_name, amount= item_amount ,buy_price= [item_buy_price], buy_date= [item_buy_date], expiration= [item_expiration], sale_price= [item_sale_price], sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))

            else:
                if item_buy_date >= start_date and item_buy_date <= end_date:
                    if item_name in name_list and item_name not in expired_name_list and item_expired:
                        expired_name_list.append(item_name)
                        name_item_list.append(
                            ItemByName(name= item_name, amount= item_amount ,buy_price= [item_buy_price], buy_date= [item_buy_date], expiration= [item_expiration], sale_price= [item_sale_price], sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
                    elif item_name in name_list and not item_expired:
                        for class_item in name_item_list:
                            if class_item.name == item_name and class_item.expired == item_expired:
                                class_item.amount = class_item.amount + item_amount
                                class_item.buy_price = make_classlist(class_item.buy_price, item_buy_price)
                                class_item.buy_date = make_classlist(class_item.buy_date, item_buy_date)
                                class_item.expiration = make_classlist(class_item.expiration, item_expiration)
                                class_item.sale_price = make_classlist(class_item.sale_price, item_sale_price)
                                class_item.sold = class_item.sold + item_sold
                                class_item.remaining = class_item.remaining if item_expired else class_item.remaining + item_remaining
                                class_item.profit = class_item.profit + item_profit
                    elif item_name not in name_list and item_name in expired_name_list and not item_expired:
                        name_list.append(item_name)
                        name_item_list.append(
                            ItemByName(name= item_name, amount= item_amount ,buy_price= [item_buy_price], buy_date= [item_buy_date], expiration= [item_expiration], sale_price= [item_sale_price], sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
                    elif item_name in expired_name_list:
                        for class_item in name_item_list:
                            if class_item.name == item_name and class_item.expired == item_expired:
                                class_item.amount = class_item.amount + item_amount
                                class_item.buy_price = make_classlist(class_item.buy_price, item_buy_price)
                                class_item.buy_date = make_classlist(class_item.buy_date, item_buy_date)
                                class_item.expiration = make_classlist(class_item.expiration, item_expiration)
                                class_item.sale_price = make_classlist(class_item.sale_price, item_sale_price)
                                class_item.sold = class_item.sold + item_sold
                                class_item.remaining = class_item.remaining + item_remaining
                                class_item.profit = class_item.profit + item_profit
                    else:
                        if item_expired:
                            expired_name_list.append(item_name)
                        elif not item_expired:
                            name_list.append(item_name)
                        name_item_list.append(
                            ItemByName(name= item_name, amount= item_amount ,buy_price= [item_buy_price], buy_date= [item_buy_date], expiration= [item_expiration], sale_price= [item_sale_price], sold= item_sold, remaining= item_remaining, expired= item_expired, profit= item_profit))
                
        return name_item_list


#---------------- RETRIEVING INFORMATION FROM AN EXTERNAL FILE ----------------#
def import_data(file, csv_file, date, append=False, overwrite=False):
    #The first section converts the file to a list of dictionaries for easier import
    extension = file.split('.')[-1].lower()
    if extension == 'csv':
        data_dict_list = dict_list_csv(file)
        cf = pd.read_csv(file)
        from_columns = list(cf.columns)
    elif extension == 'xlsx':
        xld =pd.read_excel(file, sheet_name = None)
        #xld will always return a dict bc of None
        sheet_list = list(xld)
        if len(sheet_list) > 1:
            sheet = input(f'Which sheet from {sheet_list} will be imported? \nPlease enter a name or index, \nIf it is the first sheet you can simply press enter:')
            selected_sheet = 0 if not sheet else sheet
            try:
                xlf =pd.read_excel(file,sheet_name = selected_sheet)
            except:
                try:
                    xlf =pd.read_excel(file,sheet_name = int(selected_sheet))
                except:
                    CONSOLE.print('The program will automatically grab the fist page as no valid page was given')
                    xlf =pd.read_excel(file,sheet_name = sheet_list[0])
        else:
            xlf =pd.read_excel(file,sheet_name = sheet_list[0])
        data_dict_list= xlf.to_dict('records')
        from_columns = xlf.columns.tolist()
    elif extension == 'json':
        with open(file) as json_file:
            jsondata = json.load(json_file)
            if type(jsondata) == dict: #format in json_a_test
                if len(list(jsondata)) > 1:
                    j_section = input(f'Please name the section to convert\n{list(jsondata)} : ')
                    data_dict_list = jsondata[j_section]
                else:
                    data_dict_list = jsondata[list(jsondata)[0]]
            elif type(jsondata) == list: #format in json_b_test
                data_dict_list = jsondata
            from_columns = list(data_dict_list[0].keys())
    else:
        CONSOLE.print('Please select a valid file to import')
        return False
    
    csv_headers = list(pd.read_csv(csv_file).columns)
    key_check = same_names(csv_file, from_columns) 
    eq = {}
    
    if not key_check:
        return False
    elif isinstance(key_check, list): 
        for x in range(len(key_check)):
            eq[csv_headers[x]] = key_check[x]
    example = data_dict_list[-1]

    if csv_file == 'bought.csv':
        warning = ("If your inventory contained product id's the append section will override that with it's own id's")
        date_key = 'buy_date' if not eq else eq['buy_date']
    elif csv_file == 'sold.csv':
        warning = ("If your document contained it's own product id's appending this could cause conflict")
        date_key = 'sell_date' if not eq else eq['sell_date']
    elif csv_file == 'prices.csv':
        warning = ("If your document contained it's own product id's appending this could cause conflict with the data")
        date_key = 'price_date' if not eq else eq['price_date']
    
    date_txt = example[date_key]
    date_format = False   
    if to_ymd(date_txt):
        pass
    else:
        CONSOLE.print('The dates on your file do not seem to have a "%Y-%m-%d" format')
        order = input('Please establish the date format separating the order by spaces\nexample: month day year: ')
        order= order.split()
        date_format = get_date_format(date_txt, order)
        if not date_format:
            CONSOLE.print('The date format provided is not valid, the import has beed cancelled to prevent fatal data corruption, please retry')
            return False
    if append:
        CONSOLE.print(warning)
    elif overwrite:
        wipe_csv(csv_file,date,csv_headers)

    if csv_file == 'bought.csv':
        for i in data_dict_list:
            buy_date = convert_to_ymd_txt(i[date_key], date_format) if date_format else i[date_key]
            exp_key = 'expiration_date' if not eq else eq['expiration_date']
            exp_date = convert_to_ymd_txt(i[exp_key], 
                    date_format) if date_format else i[exp_key]

            if append:
                if key_check and not eq:
                    
                    try:
                        buy(i['product_name'], i['amount'], buy_date, i['buy_price'], exp_date, sell_price= i['sell_price'])
                    except:
                        try:
                            buy(i['product_name'], i['amount'], buy_date, i['buy_price'], exp_date, sell_price= i['sale_price'])
                        except:
                            try:
                                buy(i['product_name'], i['amount'], buy_date, i['buy_price'], exp_date, sell_price= i['price'])
                            except:
                                buy(i['product_name'], i['amount'], buy_date, i['buy_price'],expiration_date= exp_date)
                elif key_check and eq:
                    buy(i[eq['product_name']], i[eq['amount']],buy_date, i[eq['buy_price']], exp_date)

            
            elif overwrite:
                if key_check and not eq:
                    try:
                        buy(i['product_name'], i['amount'], buy_date, i['buy_price'], exp_date, id = i['id'], sell_price= i['sell_price'])
                    except:
                        try:
                            buy(i['product_name'], i['amount'], buy_date, i['buy_price'], exp_date, id = i['id'], sell_price= i['sale_price'])
                        except:
                            try:
                                buy(i['product_name'], i['amount'],buy_date, i['buy_price'], exp_date, id = i['id'], sell_price= i['price'])
                            except:
                                try:
                                    buy(i['product_name'], i['amount'], buy_date, i['buy_price'],exp_date,  id = i['id'])
                                except:
                                    buy(i['product_name'], i['amount'],buy_date, i['buy_price'], exp_date)
                elif key_check and eq:
                    try:
                        buy(i[eq['product_name']], i[eq['amount']], buy_date, i[eq['buy_price']], exp_date, id = i[eq['id']])
                    except:
                        buy(i[eq['product_name']], i[eq['amount']], buy_date, i[eq['buy_price']], exp_date)


    else:
        if date_format:
            for i in data_dict_list:
                print(date_format)
                i[date_key] = convert_to_ymd_txt(i[date_key], date_format)

        fieldnames = csv_headers if not eq else list(eq.values())
        with open(csv_file, 'a') as import_file:
                writer = csv.DictWriter(import_file, fieldnames= fieldnames )
                for row in data_dict_list:
                        writer.writerow(row)
        #this happens for both append and overwrite because the file wiping has already been handled
    CONSOLE.print('The import has been completed')