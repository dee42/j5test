#!/usr/bin/env python

from j5.Basic import Decorators
# import Skipped exception classes from supported frameworks - see Skipped below
try:
    from py.__.test.outcome import Skipped as PyTestSkipped
except ImportError:
    class PyTestSkipped(object):
        pass
try:
    from nose.plugins.skip import SkipTest as NoseSkipped
except ImportError:
    class NoseSkipped(object):
        pass
import sys
import os
import logging

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
    """raise AssertionError, if target code raises the given unexpected exception"""
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

class NotImplementedTest(Skipped):
    """A class to indicate that the reason the test was skipped is that it is not implemented"""
    pass

def skip(msg="unknown reason"):
    """Raises a generic Skipped exception that will cause this test to be skipped"""
    raise Skipped(msg)

def if_check(check, check_description=None):
    """A decorator that skips the underlying function if check() doesn't return True"""
    if check_description is None:
        check_description = check.__doc__
    try:
        check_result = check()
        check_error = False
    except Exception, e:
        check_error = True
    if check_error:
        @Decorators.decorator
        def if_check(target, *args, **kwargs):
            logging.error("Test depends on %s which failed with %s" % (check_description, e))
            raise e
        return if_check
    elif not check_result:
        @Decorators.decorator
        def if_check(target, *args, **kwargs):
            raise Skipped("Test depends on %s" % check_description)
        return if_check
    else:
        # don't alter the function if not necessary
        def if_check(target):
            return target
        return if_check

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

def if_executable(*required_executables):
    """A decorator that skips the underlying function if the given executable files are not all accessible (ANDs the results)"""
    # NOTE: This doesn't test the permissions of the executables, just if the files are present
    found_all = True
    missing_executable = None
    for executable in required_executables:
        found = False
        if os.path.isabs(executable):
            found = os.path.exists(executable)
        else:
            for search_path in os.defpath.split(os.pathsep):
                if os.path.exists(os.path.join(search_path, executable)):
                    found = True
                    break
        if not found:
            missing_executable = executable
            found_all = False
            break
    if not found:
        @Decorators.decorator
        def if_executable(target, *args, **kwargs):
            raise Skipped("Test is marked not to run if executable %s is not present" % (missing_executable,))
        return if_executable
    else:
        # don't alter the function if not necessary
        def if_executable(target):
            return target
        return if_executable

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
            raise AssertionError("Call to %s did not raise %s but raised %s: %s" % \
                  (target.__name__, ExpectedException.__name__, e.__class__.__name__, e))
        raise AssertionError("Call to %s did not raise %s but returned %r" % \
              (target.__name__, ExpectedException.__name__, result))
    return expect_external_error_for

def skip_test_for(msg, check_args):
    """on calls passing the check_args specification, skip the test with the given message
    check_args(target, *args, **kwargs) should be a callable that returns whether to skip the test"""
    @Decorators.decorator
    def skip_test_for(target, *args, **kwargs):
        if not check_args(target, *args, **kwargs):
            return target(*args, **kwargs)
        skip(msg)
    return skip_test_for
