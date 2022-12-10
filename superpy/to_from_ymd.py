from datetime import date
from datetime import datetime
import itertools

def to_ymd(str_date):
    try:
        date_obj =datetime.strptime(str_date, '%Y-%m-%d').date()
        return date_obj
    except:
        raise TypeError('The given information is not in yyyy-mm-dd format')


def from_ymd(date_obj):
    try:
        str_date =datetime.strftime(date_obj, '%Y-%m-%d')
        return str_date
    except:
        raise TypeError('The given information is not in yyyy-mm-dd format')


def get_date_format(s_date, order):
    days_f= ['%d','%-d','%a', '%A', '%w', ]
    months_f =['%m', '%-m', '%b', '%B']
    years_f = ['%-y', '%Y']
    for x,i in enumerate(order):
        if i == 'day':
            order[x] = days_f
        elif i == 'month':
            order[x] = months_f
        elif i == 'year':
            order[x] = years_f
    date_patterns = list(itertools.product(order[0],order[1],order[2]))
    
    for pattern in date_patterns:
        txt_format_a = (f'{pattern[0]}-{pattern[1]}-{pattern[2]}')
        txt_format_b = (f'{pattern[0]} {pattern[1]} {pattern[2]}')
        txt_format_c = (f'{pattern[0]}/{pattern[1]}/{pattern[2]}')
        try:
            datetime.strptime(s_date, txt_format_a).date()
            return txt_format_a
        except:
            try:
                datetime.strptime(s_date, txt_format_b).date()
                return txt_format_b
            except:
                try:
                    datetime.strptime(s_date, txt_format_c).date()
                    return txt_format_c
                except:
                    pass
    print('Date is not in any of the expected formats')
    return False

def convert_to_ymd_txt(s_date, date_format):
    date_obj = datetime.strptime(s_date, date_format).date()
    str_date =datetime.strftime(date_obj, '%Y-%m-%d')
    return str_date