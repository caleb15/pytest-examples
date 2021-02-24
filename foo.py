from call_api import api_call
from call_api import APICaller
from random import randint

def get_large_random_number():
    return randint(0,9999999999)

def do_foo():
    return api_call()

def do_foo_class():
    my_api_caller = APICaller()
    return my_api_caller.api_call()