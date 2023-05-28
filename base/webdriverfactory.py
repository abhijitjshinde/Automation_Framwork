"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
import traceback
from selenium import webdriver
from selenium.webdriver.common.service import Service
import os
import utilities.custom_logger as cl
import logging
from utilities.util import Util

class WebDriverFactory():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, browser):
        """
        Inits WebDriverFactory class

        Returns:
            None
        """
        self.browser = browser
    """
        Set chrome driver and iexplorer environment based on OS

        chromedriver = "C:/.../chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

        PREFERRED: Set the path on the machine where browser will be executed
    """

    def getWebDriverInstance(self):
        """
       Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """
        util = Util()
        # conf_file = configparser.ConfigParser()
        # conf_file.read("configfiles/project_configuration.ini")
        baseURL = util.getConfig('URL', 'testurl')  #Test Url fetch from config file
        # baseURL = "https://abc.com/"  #Test Url
        # baseURL = "https://abc_prod.com/"  #Production Url
        chromedriver = util.getConfig('DriverExe','chromeDriver')
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            # Set chrome driver
            os.environ["webdriver.chrome.driver"] = chromedriver
            # chdrive = Service(chromedriver)
            driver = webdriver.Chrome(chromedriver)
        else:
            os.environ["webdriver.chrome.driver"] = chromedriver
            # chdrive = Service(chromedriver)
            driver = webdriver.Chrome(chromedriver)
        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(3)
        # Maximize the window
        driver.maximize_window()
        # Loading browser with App URL
        driver.get(baseURL)
        self.log.info("### Selected URL is " + baseURL)
        return driver
