#!/usr/bin/env python

from j5.Test import Utils

# some helper code for the tests

class SubvalueError(ValueError):
    pass

def sample_method(option):
    if option == 1:
        return "pigeons"
    elif option == 2:
        raise ValueError("Wrong value")
    elif option == 3:
        raise SubvalueError("Wrong subvalue")
    elif option == 4:
        raise KeyError("Wrong key")

@Utils.method_raises(ValueError)
def sample_decorated_function(option):
    if option == 1:
        return "pigeons"
    elif option == 2:
        raise ValueError("Wrong value")
    elif option == 3:
        raise SubvalueError("Wrong subvalue")
    elif option == 4:
        raise KeyError("Wrong key")

# here are the actual tests
def test_simple_raises_correct():
    """check raising the correct error, and a subclass of the correct error"""
    assert Utils.raises(ValueError, sample_method, 2)
    assert Utils.raises(ValueError, sample_method, 3)

def test_simple_raises_returns():
    """check returning a value causes an error in raises"""
    raised = None
    returned = None
    try:
        returned = Utils.raises(ValueError, sample_method, 1)
    except AssertionError, e:
        raised = e
    except StandardError, e:
        raised = e
    assert returned is None
    assert isinstance(raised, AssertionError)
    assert "Call to sample_method did not raise ValueError but returned 'pigeons'" == str(raised)

def test_simple_raises_incorrect():
    """checks that raises handles an incorrect exception properly"""
    raised = None
    returned = None
    try:
        returned = Utils.raises(ValueError, sample_method, 4)
    except AssertionError, e:
        raised = e
    except StandardError, e:
        raised = e
    assert returned is None
    assert isinstance(raised, AssertionError)
    print str(raised)
    assert "Call to sample_method did not raise ValueError but raised KeyError: 'Wrong key'" == str(raised)

def test_method_raises_correct():
    """check method_raises works with raising the correct error, and a subclass of the correct error"""
    assert sample_decorated_function(2)
    assert sample_decorated_function(3)

def test_method_raises_returns():
    """check returning a value causes an error in method_raises"""
    raised = None
    returned = None
    try:
        returned = sample_decorated_function(1)
    except AssertionError, e:
        raised = e
    except StandardError, e:
        raised = e
    assert returned is None
    assert isinstance(raised, AssertionError)
    assert "Call to sample_decorated_function did not raise ValueError but returned 'pigeons'" == str(raised)

def test_method_raises_incorrect():
    """checks that method_raises handles an incorrect exception properly"""
    raised = None
    returned = None
    try:
        returned = sample_decorated_function(4)
    except AssertionError, e:
        raised = e
    except StandardError, e:
        raised = e
    assert returned is None
    assert isinstance(raised, AssertionError)
    print str(raised)
    assert "Call to sample_decorated_function did not raise ValueError but raised KeyError: 'Wrong key'" == str(raised)

