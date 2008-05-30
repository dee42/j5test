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

def raises(ExpectedException, target, *args, **kwargs):
    """raise AssertionError, if target code does not raise the expected exception"""
    try:
        result = target(*args, **kwargs)
    except ExpectedException, e:
        return True
    except StandardError, e:
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
    @Decorators.decorator
    def if_module(target, *args, **kwargs):
        if not ConditionalModule:
            raise Skipped("Test depends on presence of module %s" % module_name)
        return target(*args, **kwargs)
    return if_module

