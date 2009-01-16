# -*- coding: utf-8 -*-

"""Test module for nose tests helper"""

from j5.Test import NoseTests
import j5.Test
from j5.OS import ThreadControl
from j5.Test import SampleNoseTests
from j5.Test import SampleNoseTestsFailure

def test_default_config():
    config = NoseTests.get_default_config()
    assert config.verbosity == 2
    assert config.includeExe == True

def test_get_test_loader():
    loader = NoseTests.get_package_test_loader(j5.Test)
    suite = loader.loadTestsFromName('.')
    assert suite.countTestCases() > 50
    loader = NoseTests.get_module_test_loader(SampleNoseTests)
    suite = loader.loadTestsFromName(SampleNoseTests.__name__)
    assert suite.countTestCases() == 1
    loader = NoseTests.get_named_module_test_loader(SampleNoseTests.__file__)
    suite = loader.loadTestsFromName(SampleNoseTests.__name__)
    assert suite.countTestCases() == 1

def test_run_tests_works():
    loader = NoseTests.get_module_test_loader(SampleNoseTests)
    suite = loader.loadTestsFromName(SampleNoseTests.__name__)
    assert NoseTests.run_tests(suite=suite)

def test_run_tests_fails_on_error():
    loader = NoseTests.get_module_test_loader(SampleNoseTestsFailure)
    suite = loader.loadTestsFromName(SampleNoseTestsFailure.__name__)
    assert suite.countTestCases() == 1
    assert not NoseTests.run_tests(suite=suite)

