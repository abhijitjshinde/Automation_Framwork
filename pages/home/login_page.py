from base.basepage import BasePage
import utilities.custom_logger as cl
from utilities.util import Util
import logging

class LoginPage(BasePage):
    log = cl.customLogger(logging.DEBUG)
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    #Locators
    _Username_texbox = "username"
    _password_texbox = "password"
    _Login_button = "Login"
    _profile_icon = "uiImage"
    _Login_errorMsg = "//div[@id = 'error']"
    _error_dialogbox_crossbtn = "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/button/lightning-icon"
    _logout_link = "Log Out"
    _lightningExperience = "Switch to Lightning Experience"  # link



    def enterUsername(self,username):
        self.sendKeys(username,self._Username_texbox)

    def enterpassword(self,password):
        self.sendKeys(password,self._password_texbox)

    def clickLoginButton(self):
        self.elementClick(self._Login_button)

    def clickLightninglink(self):
        self.elementClick(locator=self._lightningExperience,locatorType="link")

    def checklightningpage(self):
        self.util.sleep(2)
        if self.isElementPresent(locator=self._lightningExperience,locatorType="link") == True:
            print("################## element present")
            self.clickLightninglink()

    def clearTextfields(self):
        self.elementClear(locator=self._Username_texbox)
        self.elementClear(locator=self._password_texbox)

    def Loginsucessful(self):
        result = self.isElementPresent(self._profile_icon,locatorType="class")
        return result

    def Loginfail(self):
        EL = self.waitForElement(self._Login_errorMsg,locatorType="xpath")
        if EL != None:
            actual_errortext = self.getText(locator=self._Login_errorMsg,locatorType="xpath")
            if actual_errortext == "Please check your username and password. If you still can't log in, contact your Salesforce administrator.":
                result = False
        else:
            result = True
        return result
    def login(self, username, password):
        print(username,"---->",password,"-------------------------")
        self.enterUsername(username)
        self.enterpassword(password)
        self.clickLoginButton()
        self.util.sleep(1)
        self.checklightningpage()

    def logout(self):
        if self.isElementPresent(self._profile_icon,locatorType="class") == True:
            self.elementClick(locator=self._profile_icon,locatorType="class")
            self.elementClick(locator=self._logout_link,locatorType="link")
        else:
            self.log.error("Locator is not found :: "+self._profile_icon)

    def verifyLoginTitle(self):
        self.errorDialogCross()
        result = self.verifyPageTitle("Home | Salesforce")
        self.util.sleep(1)
        return result
    def errorDialogCross(self):
        self.waitForElement(locator=self._error_dialogbox_crossbtn, locatorType="xpath",timeout=5)
        if self.isElementPresent(locator=self._error_dialogbox_crossbtn, locatorType="xpath") == True:
            self.elementClick(locator=self._error_dialogbox_crossbtn, locatorType="xpath")
        else:
            self.log.info("Error Dialog is not found... ")
