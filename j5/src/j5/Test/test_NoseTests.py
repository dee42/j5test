# -*- coding: utf-8 -*-

"""Test module for nose tests helper"""

from j5.Test import NoseTests
import j5.Test
from j5.OS import ThreadControl

def test_default_config():
    config = NoseTests.get_default_config()
    assert config.verbosity == 2
    assert config.includeExe == True

def test_get_test_loader():
    loader = NoseTests.get_module_test_loader(j5.Test)
    suite = loader.loadTestsFromName('.')
    assert suite.countTestCases() > 50

