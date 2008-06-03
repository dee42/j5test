#!/usr/bin/env python

from j5.Test import Utils
import sys

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

@Utils.method_not_raises(KeyError)
def sample_decorated_function_2(option):
    if option == 1:
        return "pigeons"
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

def test_simple_not_raises_returns():
    """check returning a value doesn't cause an error in not_raises"""
    assert Utils.not_raises(ValueError, sample_method, 1)

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

def test_method_not_raises_correct():
    """check method_not_raises works with returning a value"""
    assert sample_decorated_function_2(1) == "pigeons"

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

def test_method_not_raises_incorrect():
    """check method_not_raises works with returning a value"""
    raised = None
    returned = None
    try:
        returned = sample_decorated_function_2(4)
    except AssertionError, e:
        raised = e
    except StandardError, e:
        raised = e
    assert returned is None
    assert isinstance(raised, AssertionError)
    print str(raised)
    assert "Call to sample_decorated_function_2 raised KeyError: 'Wrong key'" == str(raised)

def test_skiptest():
    """checks that this method will be skipped"""
    assert True
    Utils.skip("This method should be skipped, as it is testing skipping methods")
    raise AssertionError("This test should have been skipped")

@Utils.method_raises(Utils.Skipped)
def test_catchskip():
    """Tests that a properly decorated method is skipped - this must be run..."""
    assert True
    Utils.skip("This method should be skipped, as it is testing skipping methods")
    raise AssertionError("This test should have been skipped")

@Utils.method_raises(Utils.Skipped)
@Utils.if_module(None, "Badgers")
def test_conditional_module_missing():
    """Tests that this test is not run..."""
    raise AssertionError("This test should have been skipped with a message about the Badgers module""")

@Utils.method_not_raises(Utils.Skipped)
@Utils.if_module(Utils, "j5.Test.Utils")
def test_conditional_module_present():
    """Tests that this test is run..."""
    assert True


@Utils.method_raises(Utils.Skipped)
@Utils.if_platform("Badgers")
def test_conditional_platform_missing():
    """Tests that this test is not run..."""
    raise AssertionError("This test should have been skipped with a message about the platform""")

@Utils.method_not_raises(Utils.Skipped)
@Utils.if_platform("a", "few", sys.platform)
def test_conditional_platform_present():
    """Tests that this test is not run..."""
    assert True

def test_expected_external_error_for():
    """Checks that expected errors are skipped when the right options are passed"""
    wrapper = Utils.expected_external_error_for(KeyError, "Key errors for 4", option=4)(sample_method)
    assert Utils.method_raises(Utils.ExpectedExternalError)(wrapper)(4)
    assert Utils.method_raises(Utils.ExpectedExternalError)(wrapper)(option=4)
    assert Utils.method_raises(ValueError)(wrapper)(option=3)
    assert wrapper(1) == "pigeons"
    assert wrapper(option=1) == "pigeons"

