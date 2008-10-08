# -*- coding: utf-8 -*-

"""Utility functions to help with working with nose
with our default configuration (i.e. something like py.test)"""

from nose import config
from nose import loader

import os
import re

def get_default_config(**kwargs):
    """Returns a configuration file set up with our default settings
    Extra arguments can be passed in through kwargs"""
    kwargs.setdefault("verbosity", 2)
    kwargs.setdefault("includeExe", True)
    kwargs.setdefault("testMatch", re.compile("^[Tt]est"))
    return config.Config(**kwargs)

def get_module_test_loader(base_module):
    """Takes a base module, and returns a loader already loaded with tests, ready for a TestRunner
    e.g. "import j5 ; ld = get_module_test_loader(j5)" will get all tests under j5"""
    workingDir = os.path.dirname(base_module.__file__)
    cfg = get_default_config(workingDir=workingDir)
    return loader.TestLoader(config=cfg)

