#!/usr/bin/env python

from j5.Basic import Decorators

def raises(ExpectedException, target, *args, **kwargs):
    """raise AssertionError, if target code does not raise the expected exception"""
    try:
        result = target(*args, **kwargs)
    except ExpectedException, e:
        return True
    except StandardError, e:
        raise AssertionError("Call to %s did not raise %s but raised %s: %s" % (target.__name__, ExpectedException.__name__, e.__class__.__name__, e))
    raise AssertionError("Call to %s did not raise %s but returned %r" % (target.__name__, ExpectedException.__name__, result))

def method_raises(ExpectedException):
    """A decorator that ensures that the underlying function raises the ExpectedException"""
    @Decorators.decorator
    def method_raises(target, *args, **kwargs):
        return raises(ExpectedException, target, *args, **kwargs)
    return method_raises

