#!/usr/bin/env python

from j5.Test import IterativeTester
import sys
import selenium
import logging
# FIXME: remove this once we don't do naughty things
import inspect

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
        self._selenium_runners = {}
        havebrowsers = False
        for browser in all_browsers:
            if selenium_can_find(browser):
                havebrowsers = True
                self._browsernames[browser] = browser
                self._resources[browser] = None
        if not havebrowsers:
            self._skipped_conditions["NoBrowsers"] = "No working browsers to run tests with"

    def setup(self):
        # TODO: start selenium server automatically
        # FIXME: This is obviously abysmal
        frame = inspect.currentframe()
        # this is designed specifically for j5.Control.test_WebServer
        web_dimension = frame.f_back.f_locals["dims"][0]
        self.browser_urls = {}
        for web_config_name in web_dimension.configs.keys():
            web_config = web_dimension.configs[web_config_name]
            app_config = web_config.get_rootnode()[web_dimension.application]
            app_web_config = app_config.get_value(web_config.get_path(), {})
            host = getattr(web_config, "host", "localhost")
            port = getattr(web_config, "port", 8080)
            baseurl = getattr(web_config, "baseurl", "")
            if baseurl != "" and not baseurl.endswith("/"):
                baseurl += "/"
            app_baseurl = getattr(app_web_config, "baseurl", "")
            baseurl += app_baseurl
            if baseurl != "" and not baseurl.endswith("/"):
                baseurl += "/"
            self.browser_urls[web_config_name] = "http://%s:%s/%s" % (host, str(port), baseurl)

    def start_browser(self, browsername, web_config_name):
        """starts up a browser for the given web config"""
        selenium_runner = selenium.selenium(self.seleniumHost, self.seleniumPort, "*%s" % browsername, self.browser_urls[web_config_name])
        selenium_runner.start()
        self._selenium_runners[browsername, web_config_name] = selenium_runner
        return selenium_runner

    def get_browser(self, browser_name, web_config_name):
        """gets a controllable browser for the given browser and webserver"""
        if (browser_name, web_config_name) in self._selenium_runners:
            return self._selenium_runners[browser_name, web_config_name]
        return self.start_browser(browser_name, web_config_name)

    def setup_method(self, browsername):
        # FIXME: provide a SANE way to pass in the config and use it to set the host and port for browserURL
        # TODO: work out a sane way to get the current web plugin dimension
        frame = inspect.currentframe()
        web_config_name = frame.f_back.f_locals["varnames"][0]
        logging.warning("Browser URL for %s is %s" % (web_config_name, self.browser_urls[web_config_name]))
        self._resources[browsername] = self.get_browser(browsername, web_config_name)

    def teardown_method(self, browsername):
        # self._resources[browsername].stop()
        pass

    def teardown(self):
        """stops any running browsers"""
        for browsername, web_config_name in self._selenium_runners.keys():
            selenium = self._selenium_runners.pop((browsername, web_config_name))
            selenium.stop()



