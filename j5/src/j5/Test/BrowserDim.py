#!/usr/bin/env python

from j5.Test import IterativeTester
import sys
import selenium

# this stuff should be added to the selenium package as a patch, to support discovery of browsers
all_browsers = ["firefox", "iexplore", "safari", "iehta", "chrome", "opera", "piiexplore", "pifirefox", "konqueror", "mock"]
def selenium_can_find(browser_name):
    return browser_name == "firefox"

class BrowserDim(IterativeTester.Dimension):
    seleniumHost = "localhost"
    seleniumPort = 4444
    def __init__(self):
        """iterates over supported browsers and runs tests on each of them"""
        browsernames = []
        self._resources = {}
        self._browsernames = {}
        self._skipped_conditions = {}
        havebrowsers = False
        for browser in all_browsers:
            if selenium_can_find(browser):
                havebrowsers = True
                self._browsernames[browser] = browser
                self._resources[browser] = None
        if not havebrowsers:
            self._skipped_conditions["NoBrowsers"] = "No working browsers to run tests with"

    def setup_class(cls):
        # TODO: start selenium server automatically
        pass

    def setup_method(self, browsername):
        # FIXME: provide a SANE way to pass in the config and use it to set the host and port for browserURL
        import inspect
        frame = inspect.currentframe()
        # browserURL = "http://%s:%s/" % (browserHost, browserPort)
        # this is designed specifically for j5.Control.test_WebServer
        # FIXME: This is obviously abysmal
        browserURL = frame.f_back.f_locals["self"].get_webtest_url()
        selenium_runner = selenium.selenium(self.seleniumHost, self.seleniumPort, "*%s" % browsername, browserURL)
        selenium_runner.start()
        self._resources[browsername] = selenium_runner

    def teardown_method(self, browsername):
        self._resources[browsername].stop()


