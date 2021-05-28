import pytest

from lambda_function.create_cw_event import say_hello

def test_hello():
    s = say_hello()
    assert("hello", s)