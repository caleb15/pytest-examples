import foo

# This file uses pytest-mock library
# If you don't want to use pytest-mock
# then you can use vanilla "mock"
# ex:
"""
from unittest import mock
from fah import do_stuff
def test():
    with mock.patch('fah.foo'):
        do_stuff()

# or:
@mock.patch('fah.foo')
def test(mocker):
    do_stuff()
"""

def test_patch_library_function(mocker):
    mocker.patch('foo.randint', return_value=0)
    assert foo.get_large_random_number() == 0

# unlike regular mocker pytest mocker can't be used with "with"
# def test_count_calls(mocker):
#     with mocker.patch('foo.randint') as m:
#         foo.get_large_random_number()
#         m.assert_called_once()

# instead you should just get ref directly
def test_count_calls(mocker):
    m=mocker.patch('foo.randint')
    foo.get_large_random_number()
    # foo.get_large_random_number() # uncommenting this would correctly cause test to fail
    m.assert_called_once()

def test_patch_foo(mocker):
    mocker.patch('foo.api_call')
    foo.do_foo()

def test_patch_foo_with_val(mocker):
    mocker.patch('foo.api_call', return_value=3)
    assert foo.do_foo() == 3

def test_patch_object(mocker):
    # same thing as just .patch except you can pass object in directly
    # instead of doing .patch('foo.api_call')
    mocker.patch.object(foo, 'api_call')
    foo.do_foo()