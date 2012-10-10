#!/usr/bin/env python

import threading
import contextlib
from functools import wraps
import sys

class ConditionAvoidanceSignal(Exception):
    pass

class ConditionAvoidance:
   def __setattr__(self, a, b):
       if isinstance(b, ConditionAvoidance):
           raise ConditionAvoidanceSignal()

class ConditionalContextManager(object):
    """Helper for @conditionalcontextmanager decorator."""
    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        try:
            return self.gen.next()
        except StopIteration, e:
            # set flag
            return ConditionAvoidance()

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                self.gen.next()
            except StopIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type()
            if isinstance(value, ConditionAvoidanceSignal):
                return True
            try:
                self.gen.throw(type, value, traceback)
                raise RuntimeError("generator didn't stop after throw()")
            except StopIteration, exc:
                # Suppress the exception *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed
                return exc is not value
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is not value:
                    raise


def conditionalcontextmanager(func):
    """@conditionalcontextmanager decorator.

    Typical usage:

        @conditionalcontextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                if condition:
                    yield <value>
            finally:
                <cleanup>

    This makes this:

        with some_generator(<arguments>) as stopper.<variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            if condition:
                <variable> = <value>
                <body>
        finally:
            <cleanup>

    """
    @wraps(func)
    def helper(*args, **kwds):
        return ConditionalContextManager(func(*args, **kwds))
    return helper

