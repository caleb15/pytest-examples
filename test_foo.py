import foo
import json
import pytest

# This file uses pytest-mock library
# If you don't want to use pytest-mock
# then you can use vanilla "mock"
# ex:
"""
from unittest import mock
from fah import do_stuff
def test():
    with mock.patch('fah.foo'):
        do_stuff() # foo is safely mocked in do_stuff
    do_stuff() # <- 'foo' would not get mocked in this call'!
    # only calls in the with block get mocked

# or:
@mock.patch('fah.foo')
def test(mocker):
    do_stuff()
"""

# patch path examples


def test_patch_standard_library_function(mocker):
    # the import: from random import randint
    # because import is in foo we need to reference it with foo
    mocker.patch("foo.randint", return_value=0)
    assert foo.get_large_random_number() == 0


def test_patch_func_from_another_file(mocker):
    # Even tho "api_call" is in "call_api" file
    # We still reference it via "foo.api_call"
    # The import: from call_api import api_call
    m = mocker.patch("foo.api_call")
    foo.do_foo() == m


def test_patch_json_dumps_bad(mocker):
    # The import: import json
    # usage: json.dumps()
    # below would be incorrect because "dumps" is not a property of the "foo" module,
    # it's a property of "json"
    with pytest.raises(AttributeError):
        m = mocker.patch("foo.dumps")


def test_patch_json_dumps_bad_2(mocker):
    # This technically works
    # but it also mocks stdlib functions in this file!
    m = mocker.patch("json.dumps")
    foo.call_json_dumps() == m  # works!
    with pytest.raises(AssertionError):
        assert json.dumps({"f": 3}) == '{"f":3}'


def test_patch_json_dumps(mocker):
    m = mocker.patch("foo.json.dumps")
    foo.call_json_dumps() == m


def test_patch_urllib(mocker):
    m = mocker.patch("foo.urllib.request")
    foo.call_urllib() == m


def test_patch_urllib_open(mocker):
    m = mocker.patch("foo.urllib.request.urlopen")
    foo.call_urllib() == m


def test_patch_object(mocker):
    # same thing as just .patch except you can pass object in directly
    # instead of doing .patch('foo.api_call')
    mocker.patch.object(foo, "api_call")
    foo.do_foo()


# other examples

# unlike regular mocker pytest mocker can't be used with "with"
# def test_count_calls(mocker):
#     with mocker.patch('foo.randint') as m:
#         foo.get_large_random_number()
#         m.assert_called_once()

# instead you should just get ref directly
def test_count_calls(mocker):
    m = mocker.patch("foo.randint")
    foo.get_large_random_number()
    # foo.get_large_random_number() # uncommenting this would correctly cause test to fail
    m.assert_called_once()


def test_patch_foo_with_val(mocker):
    mocker.patch("foo.api_call", return_value=3)
    assert foo.do_foo() == 3