#!/usr/bin/env python

"""Tests ThreadWeave"""

from j5.Test import ThreadWeave

stopper = ThreadWeave.ConditionAvoidance()
@ThreadWeave.conditionalcontextmanager
def wanneer(condition):
    if condition:
        yield

def test_condition_avoided():
    """Tests that the generator not yielding means the code block governed by with is not run"""
    code_run = False
    with wanneer(False) as stopper.detect:
        code_run = True
    assert not code_run

def test_condition_passed():
    """Tests that the generator yielding means the code block governed by with is run"""
    code_run = False
    with wanneer(True) as stopper.detect:
        code_run = True
    assert code_run

