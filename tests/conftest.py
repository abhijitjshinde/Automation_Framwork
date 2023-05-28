import pytest
import os
import time

from base.selenium_driver import SeleniumDriver
from base.webdriverfactory import WebDriverFactory
from pages.home.login_page import LoginPage
from utilities.util import Util


@pytest.fixture()
def setUp():
    print("Running method level setUp")
    yield
    print("Running method level tearDown")


@pytest.fixture(scope="class")
def oneTimeSetUp(request, browser):
    print("Running one time setUp")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()
    lp = LoginPage(driver)
    util = Util()
    username = util.getConfig('LoginCred', 'username')
    password = util.getConfig('LoginCred', 'password')
    lp.login(username, password)
    lp.errorDialogCross()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    print("Running one time tearDown")


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")

# ------------- Test result collection  for end of the Session-------------


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result
    setattr(item, "rep_" + result.when, result)


def pytest_sessionfinish(session, exitstatus):
    util = Util() #imported util class   
    for result in session.results.values():
        if result.passed:
            print("Test case has been passed ######")
            # util.sendEmail(True)
        if result.failed:
            print("Test case has been Failed ######")
            # wdf = WebDriverFactory("chrome")
            # driver = wdf.getWebDriverInstance()
            # driv = SeleniumDriver(driver)
            # driv.screenShot("SS Taken from conftest")
            # util.sendEmail(False)
        print(exitstatus)


# ------------------------------Test result collection ends here ------------------
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#
#     # set a report attribute for each phase of a call, which can
#     # be "setup", "call", "teardown"
#
#     setattr(item, "rep_" + rep.when, rep)
#
# # check if a test has failed
# @pytest.fixture(scope="function", autouse=True)
# def test_failed_check(request):
#     yield
#     # request.node is an "item" because we use the default
#     # "function" scope
#
#     if request.node.rep_setup.failed:
#         print("setting up a test failed!", request.node.nodeid)
#     elif request.node.rep_setup.passed:
#         if request.node.rep_call.failed:
#             driver = request.node.funcargs['selenium_driver']
#             sel = SeleniumDriver(driver)
#             print("Befoere taking SS ....................")
#             sel.screenShot("taken ss when Tc failed in between")
#             print("After taking SS ....................")
#             # take_screenshot(driver, request.node.nodeid)
#             print("executing test failed", request.node.nodeid)
