# -*- coding: utf-8 -*-

"""Utility functions to help with working with nose
with our default configuration (i.e. something like py.test)"""

from nose import config
from nose import loader
from nose import core
from nose import plugins

import os
import re
import sys

def get_default_config(**kwargs):
    """Returns a configuration file set up with our default settings
    Extra arguments can be passed in through kwargs"""
    kwargs.setdefault("verbosity", 2)
    kwargs.setdefault("includeExe", True)
    kwargs.setdefault("testMatch", re.compile("^[Tt]est"))
    if "plugins" not in kwargs:
        kwargs["plugins"] = plugins.DefaultPluginManager()
    return config.Config(**kwargs)

def get_module_test_loader(base_module):
    """Takes a base module, and returns a loader already loaded with tests, ready for a TestRunner
    e.g. "import j5.Test.test_NoseTests ; ld = get_package_test_loader(j5)" will get all tests under j5.Test.test_NoseTests"""
    workingDir = os.path.dirname(base_module.__file__)
    basename = os.path.basename(base_module.__file__)
    cfg = get_default_config(workingDir=workingDir)
    cfg.testNames = [basename]
    return loader.TestLoader(config=cfg)

def get_package_test_loader(base_module):
    """Takes a base package, and returns a loader already loaded with tests, ready for a TestRunner
    e.g. "import j5 ; ld = get_package_test_loader(j5)" will get all tests under j5"""
    workingDir = os.path.dirname(base_module.__file__)
    cfg = get_default_config(workingDir=workingDir)
    return loader.TestLoader(config=cfg)

def run_tests(loader=None, **kwargs):
    """Given a TestLoader, runs the tests"""
    # simple way of passing through loader with default config from above
    if loader:
        kwargs["testLoader"] = loader
    if "config" not in kwargs and loader:
        kwargs["config"] = loader.config
    # don't exit by default
    if "exit" not in kwargs:
        kwargs["exit"] = False
    # don't use sys.argv automatically
    if "argv" not in kwargs:
        kwargs["argv"] = [sys.argv[0]]
    program = core.TestProgram(**kwargs)
    return program.success

