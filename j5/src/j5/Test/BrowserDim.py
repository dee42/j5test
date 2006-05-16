#!/usr/bin/env python

from j5.Test import IEBrowser, TwillBrowser
from j5.Test import IterativeTester
import sys

class BrowserDim(IterativeTester.Dimension):
    def __init__(self, jsonly=False):
        """jsonly will make a dimension only out of those browsers which support javascript"""
        browserclasses = []
        if TwillBrowser.UseTwill:
            browserclasses.append(TwillBrowser.TwillBrowser)
        if IEBrowser.UseIE:
            browserclasses.append(IEBrowser.IEBrowser)
        self._resources = {}
        self._browserclasses = {}
        self._failed_conditions = {}
        havebrowsers = False
        for browser in browserclasses:
            if not jsonly or browser.javascript_enabled():
                havebrowsers = True
                self._browserclasses[browser.__name__] = browser
                self._resources[browser.__name__] = None

        if not havebrowsers:
            self._failed_conditions["NoBrowsers"] = "No working browsers to run tests with jsonly = %r" % jsonly

    def setup_method(self, browsername):
        self._resources[browsername] = self._browserclasses[browsername]()

    def teardown_method(self, browsername):
        self._resources[browsername].quit()


