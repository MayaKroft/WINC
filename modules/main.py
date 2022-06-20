# Do not modify these lines
__winc_id__ = '78029e0e504a49e5b16482a7a23af58c'
__human_name__ = 'modules'

# Add your code after this line

import this
import time
import datetime
import math
import sys
import greet



def wait(seconds):
    time.sleep(seconds)


def my_sin(float_arg):
    sin = math.sin(float_arg)
    return sin

def iso_now():
    iso_date = datetime.datetime.now().isoformat(timespec='minutes')  
    return iso_date


def platform():
    return sys.platform


def supergreeting_wrapper(name):
    greest = greet.super_greeting(name)
    return greest


