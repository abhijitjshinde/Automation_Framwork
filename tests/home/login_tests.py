from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
import unittest
import pytest
import sys
sys.path.insert(0, "D:/Automation_framwork/")  #Add project directory for local imports to work


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class LoginTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=2)
    def test_validLogin(self):
        self.lp.login("admin", "India@11")
        result1 = self.lp.verifyLoginTitle()
        self.ts.mark(result1, "Title is incorrect")
        result2 = self.lp.Loginsucessful()
        self.ts.markFinal("test_validLogin ", result2, "Login was successful")

    @pytest.mark.run(order=1)
    def test_invalidLogin(self):
        self.lp.logout()
        self.lp.login("kbc", "Libya@1234")
        result = self.lp.Loginfail()
        self.ts.mark(result, "Title is incorrect")
        self.lp.clearTextfields()
        # self.driver.quit()

    # test_validLogin()
