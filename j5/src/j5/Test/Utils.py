#!/usr/bin/env python

from j5.Basic import Decorators
# import Skipped exception classes from supported frameworks - see Skipped below
try:
    from py.__.test.outcome import Skipped as PyTestSkipped
except ImportError:
    PyTestSkipped = object
try:
    from nose.plugins.skip import SkipTest as NoseSkipped
except ImportError:
    PyTextSkipped = object
import sys

def raises(ExpectedException, target, *args, **kwargs):
    """raise AssertionError, if target code does not raise the expected exception"""
    try:
        result = target(*args, **kwargs)
    except ExpectedException, e:
        return True
    except Exception, e:
        raise AssertionError("Call to %s did not raise %s but raised %s: %s" % (target.__name__, ExpectedException.__name__, e.__class__.__name__, e))
    raise AssertionError("Call to %s did not raise %s but returned %r" % (target.__name__, ExpectedException.__name__, result))

def not_raises(UnexpectedException, target, *args, **kwargs):
    """raise AssertionError, if target code does not raise the unexpected exception"""
    try:
        result = target(*args, **kwargs)
    except UnexpectedException, e:
        raise AssertionError("Call to %s raised %s: %s" % (target.__name__, e.__class__.__name__, e))
    return result

def method_raises(ExpectedException):
    """A decorator that ensures that the underlying function raises the ExpectedException"""
    @Decorators.decorator
    def method_raises(target, *args, **kwargs):
        return raises(ExpectedException, target, *args, **kwargs)
    return method_raises

def method_not_raises(UnexpectedException):
    """A decorator that ensures that the underlying function does not raise the UnexpectedException"""
    @Decorators.decorator
    def method_not_raises(target, *args, **kwargs):
        return not_raises(UnexpectedException, target, *args, **kwargs)
    return method_not_raises

class Skipped(Warning, NoseSkipped, PyTestSkipped):
    """A unified class for skipping tests in any framework"""
    def __init__(self, msg):
        super(Skipped, self).__init__(msg)
        self.excinfo = None

def skip(msg="unknown reason"):
    """Raises a generic Skipped exception that will cause this test to be skipped"""
    raise Skipped(msg)

def if_module(ConditionalModule, module_name=''):
    """A decorator that skips the underlying function if ConditionalModule is not"""
    if not ConditionalModule:
        @Decorators.decorator
        def if_module(target, *args, **kwargs):
            raise Skipped("Test depends on presence of module %s" % module_name)
        return if_module
    else:
        # don't alter the function if not necessary
        def if_module(target):
            return target
        return if_module

def if_platform(*valid_platforms):
    """A decorator that skips the underlying function if not running on one of the given platforms"""
    if sys.platform not in valid_platforms:
        @Decorators.decorator
        def if_platform(target, *args, **kwargs):
            raise Skipped("Test is marked not to run on platform %s" % sys.platform)
        return if_platform
    else:
        # don't alter the function if not necessary
        def if_platform(target):
            return target
        return if_platform

class ExpectedExternalError(Skipped):
    """Raised for skipping errors that we know about, but belong to an external library"""
    pass

def contains_expected_kwargs(**match_kwargs):
    """A checker that checks if the given kwargs are present with the given values"""
    def check_expected_kwargs(target, *args, **kwargs):
        args_present = {}
        for kw, expected_value in match_kwargs.iteritems():
            actual_value = Decorators.get_or_pop_arg(kw, args, kwargs, Decorators.inspect.getargspec(target))
            if actual_value != expected_value:
                return False
            args_present[kw] = True
        return len(args_present) == len(match_kwargs)
    return check_expected_kwargs

def expect_external_error_for(ExpectedException, msg, check_args):
    """on calls passing the check_args specification, expect the given exception and skip when it is raised
    check_args(target, *args, **kwargs) should be a callable that returns whether to expect an Exception"""
    @Decorators.decorator
    def expect_external_error_for(target, *args, **kwargs):
        if not check_args(target, *args, **kwargs):
            return target(*args, **kwargs)
        try:
            result = target(*args, **kwargs)
        except ExpectedException, e:
            raise ExpectedExternalError(msg)
        except Exception, e:
            raise AssertionError("Call to %s with %s did not raise %s but raised %s: %s" % \
                  (target.__name__, match_kwargs, ExpectedEception.__name__, e.__class__.__name__, e))
        raise AssertionError("Call to %s with %s did not raise %s but returned %r" % \
              (target.__name__, match_kwargs, ExpectedException.__name__, result))
    return expect_external_error_for

