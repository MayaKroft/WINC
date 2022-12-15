from datetime import date, timedelta
from datetime import datetime
import csv
import os

#run date check will revise the last datelog when run, if it is the same day as today it will leave the log alone, if not, it will chaqnge run date withouth changing the fictional one and change new date to true, also sending a message to the user asking if they want to remain on the last ficitonla date or set it to the current one
#similar to retrieve but destined for the first run of the day and nothing more
#------------------------------ DATE LOG HANDLING -----------------------------#
#NOTE: fict date is in get date and not doc handler to prevent circular import

def fict_date(action, date = date.today(), new_date = 0, changed = 0):
    file= 'date_log.csv'
    f_path = os.path.abspath(file)
    fieldnames = ['run_date', 'fictional_date', 'date_changed']
    if action == 'write':
         with open(f_path, 'w', newline = '') as date_file:
            writer = csv.DictWriter(date_file, fieldnames= fieldnames)
            writer.writeheader()
            writer.writerow({'run_date': date, 'fictional_date': new_date, 'date_changed': changed})  
    elif action == 'read':
         with open(f_path, 'r', newline = '') as date_file:
            reader = csv.DictReader(date_file)
            last_date = [row for row in reader]
            return last_date[-1]


#-------------GLOBAL VARIABLES----------------#
LAST_LOG = fict_date('read')

def run_date_check():
    last_date = datetime.strptime(LAST_LOG['run_date'], '%Y-%m-%d').date()
    last_fake_date = datetime.strptime(LAST_LOG['fictional_date'], '%Y-%m-%d').date()
    is_changed = int(LAST_LOG['date_changed'])
    if (last_date == date.today()) and not is_changed:
        return last_date
    elif (last_date == date.today()) and is_changed:
        return last_fake_date
    elif (not last_date == date.today()) and not is_changed:
        
        fict_date('write', date.today(), date.today(), 0)
    elif (not last_date == date.today()) and is_changed:
        keep_changed = input(f'The last fictional date was {last_fake_date}, would you like to keep it(keep) or move tot he actual date (today)')
        if keep_changed == 'keep':
            fict_date('write', date.today(), last_fake_date, 1)
        if keep_changed == 'today':
            fict_date('write', date.today(), date.today(), 0)
        

def makedate(original, input):
    try:
        new_date = (original + timedelta(days = int(input))).date()
    except:
        new_date = (original + timedelta(days = int(input)))
    if new_date == date.today():
        fict_date('write', new_date= new_date, changed= 0)
    else:
        fict_date('write', new_date= new_date, changed= 1)
    return new_date

def retrieve():
    if LAST_LOG['date_changed']:
    #use date to change the strings to a date format '%Y-%m-%d'.
        sys_date = datetime.strptime(LAST_LOG['fictional_date'], '%Y-%m-%d').date()
        return sys_date
    else: 
        sys_date = datetime.strptime(LAST_LOG['run_date'], '%Y-%m-%d').date()
        return LAST_LOG['run_date']

def check_expired(expiry_date):
    current_system_date = retrieve()
    if expiry_date <= current_system_date:
        return True
    elif expiry_date > current_system_date:
        return False

def last_day_of_date(date):
    if len(date) <= 7 and len(date) > 4:
        date_obj = datetime.strptime(date, '%Y-%m').date()
        next_month = date_obj.replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        return last_day
    elif len(date) == 4:
        date_obj = datetime.strptime(date, '%Y').date()
        last_day = date_obj.replace(month = 12, day = 31)
        return last_day
    else:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return date_obj

def first_day_of_date(date):
    if len(date) <= 7 and len(date) > 4:
        date_obj = datetime.strptime(date, '%Y-%m').date()
        return date_obj
    elif len(date) == 4:
        date_obj = datetime.strptime(date, '%Y').date()
        return date_obj
    else:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return date_obj

def get_date_range(info):
    date_range = []
    if type(info) == list:
        dates = info
    else: 
        dates = [info]
    if len(dates) == 2:
        date1 = first_day_of_date(dates[0])
        date2 = last_day_of_date(dates[1])
        date_range.append(date1)
        date_range.append(date2)
        return date_range
    elif len(dates) == 1:
        date1 = first_day_of_date(dates[0])
        date2 = last_day_of_date(dates[0])
        date_range.append(date1)
        date_range.append(date2)
        return date_range

def yesterday():
    yesterday = (retrieve() - timedelta(days = 1))
    return yesterday

def tomorrow():
    tomorrow = (retrieve() + timedelta(days= 1))
    return tomorrow
