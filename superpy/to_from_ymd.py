from datetime import date
from datetime import datetime

def to_ymd(str_date):
    date_obj =datetime.strptime(str_date, '%Y-%m-%d').date()
    return date_obj

def from_ymd(date_obj):
    str_date =datetime.strftime(date_obj, '%Y-%m-%d')
    return str_date