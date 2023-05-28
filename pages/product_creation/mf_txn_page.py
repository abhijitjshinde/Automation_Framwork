from base.basepage import BasePage
import utilities.custom_logger as cl
from utilities.util import Util
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
import configparser
class MfTransaction(BasePage):

    log = cl.customLogger(logging.DEBUG)
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.util = Util()

    #Locators
    _nine_dots = "//one-app-launcher-header/button" #xpath
    _searchin = "//lightning-input/div/div/input[@placeholder = 'Search apps and items...']" #xpath
    _searchedresultBold = "//*[@id='Order_Entry__c']/div/lightning-formatted-rich-text/span/p/b" #xpath
    _header_MF = "modal-heading-01"  #id
    _dialog = "//div/section[@role = 'dialog']" #xpath
    _familyName = "//div/input[@placeholder = 'Search Lead and Families and Clients']" #xpath
    _clientName = "//div/input[@placeholder = 'Search Client']" #xpath
    _accountname = "//div/input[@placeholder = 'Search Client Account']"
    _F_C_ANameSuggList = "//ul[@role='listbox']//li/descendant::span[@class='slds-listbox__option-text slds-listbox__option-text_entity']" #xpath
    _SecondaryEmail = "email"  #name
    _canceltbtn = "//footer[@class='slds-modal__footer']/button[1]" #xpath
    _nextbtn = "//footer[@class='slds-modal__footer']/button[3]" #xpath
    _backbtn = "//footer[@class='slds-modal__footer']/button[2]" #xpath
    _addproduct = "Add Product" #name
    _lightningExperience = "Switch to Lightning Experience" #link
    _tablecontent = "//*[@id='modal-content-id-1']/div[3]/div/table/tr/td/div/div/table/tbody/tr[1]/td[3]" #xpath
    _AMCnamw = "//input[@placeholder = 'Enter AMC']" #xpath
    _SchmeName = "//input[@placeholder = 'Enter Scheme']" #xpath
    _Amount = "//input[@name= 'Amount']" #xpath
    _HoldingType = "//select[@name= 'holdingType']" #xpath
    _Folio = "//select[@class= 'select uiInput uiInputSelect uiInput--default uiInput--select']" #xpath
    _executionChannel = "//select[@name= 'Channel']" #xpath
    _AMCSearchResult = "//ul[@role='presentation']//li/div/span" #xpath
    _SaveButton = "//button[@title='Save']" #path
    _submitButton = "//button[@class='slds-button slds-button_brand']"
    _clientConsent = "//select[@name='controllerFld']"
    _ClientConsentAttachment = "//input[@name='file']"
    _ClientEmailID = "//input[@name='email']"
    _resultpagelist = "//records-record-layout-row/descendant::slot[@name='outputField']/lightning-formatted-text[@slot='outputField']"
    _test = "//div[@class='slds-scrollable_y']/table/tbody/descendant::div[@class='slds-cell-wrap']"
    _TxnID = "//records-highlights2/div[1]/div/div[1]/div[2]/h1/slot[1]/lightning-formatted-text"

    def nineDotclick(self):
        self.elementClick(locator=self._nine_dots,locatorType="xpath")

    def searchresult(self,searchText):
        # self.elementClick(locator=self._searchin,locatorType="xpath")
        self.waitForElement(locator=self._searchin,locatorType="xpath")
        self.sendKeys(searchText,self._searchin,locatorType="xpath")

    def clickBoldResult(self):
        self.elementClick(locator=self._searchedresultBold,locatorType="xpath")

    def clickmfLink(self):
        self.waitForElement(locator="MF",locatorType="link")
        self.elementClick(locator="MF",locatorType="link")
        self.util.sleep(5)
        # uncomment below line if by clicking the link  new tab opens
        # self.driver.switch_to.window(self.driver.window_handles[1])
        # self.util.sleep(7)


    def selectTheSuggResult(self,result,locator,locatorType):
        self.util.sleep(7)
        status = False
        # if self.waitForElement(locator=locator,locatorType=locatorType) == None:
        #     self.util.sleep(7)
        resultlist = self.getElementList(locator=locator, locatorType=locatorType)
        for item in resultlist:
            elementText = self.getText(element=item)
            if elementText == result:
                status = True
                self.elementClick(element=item)
        if status != False:
            return True
            self.log.info("### The Suggested item selected is "+ result)
        else:
            return False
            self.log.info("### The Suggested items is not matching with "+ result)

    def resultList(self,result,locator,locatorType,i):
        self.util.sleep(10)
        status = False
        # if self.waitForElement(locator=locator,locatorType=locatorType) == None:
        #     self.util.sleep(7)
        resultlist = self.getElementList(locator=locator, locatorType=locatorType)
        try:
            elementText = self.getText(element=resultlist[i])
            self.log.debug("Element is got from getText function :: "+elementText+ "............. ")
            # self.log.debug("### Element text found with the logic is :: " +elementText+ " and result is " + status)
            self.log.debug("This is before condition......")
            self.log.debug(elementText +" == "+result+ " ......................")
            if elementText == result:
                status = True
                self.log.debug("This is in condition...... "+str(status))
                return status
        except IndexError:
            status = False

        # for item in resultlist:
        #     elementText = self.getText(element=item)
        #     if elementText == result:
        #         status = True
        #         break
        # self.log.debug("### Element text found with the logic is :: "+str(elementText)+ " and result is "+ status)
        # if status != True:
        #     return False
        self.log.info("### The Element with text found returning :: " + str(status))
        return status
        # else:
        #     return False
        #     self.log.info("### The Element with text Not found :: " + elementText)


    def enterFamilyName(self,FamilyName):
        # FamilyName = FamilyName
        self.util.sleep(5)
        if self.waitForElement(locator=self._familyName,locatorType="xpath") != None:
            self.elementClick(locator=self._familyName,locatorType="xpath")
            self.sendKeysbywords(FamilyName,locator=self._familyName,locatorType="xpath")
        self.util.sleep(15)
        # self.waitForElement(locator=self._F_C_ANameSuggList, locatorType="xpath")
        status = self.selectTheSuggResult(FamilyName, locator=self._F_C_ANameSuggList, locatorType="xpath")
        print("############################",status)
        if status == False:
            self.elementClear(locator=self._familyName,locatorType="xpath")
            self.util.sleep(5)
            self.sendKeysbywords(FamilyName, locator=self._familyName, locatorType="xpath")
            self.util.sleep(14)
            if self.selectTheSuggResult(FamilyName, locator=self._F_C_ANameSuggList, locatorType="xpath") == False:
                self.elementClick(locator=self._familyName,locatorType="xpath")
                element = self.getElement(locator=self._familyName,locatorType="xpath")
                element.send_keys(Keys.BACKSPACE)
                self.sendKeys(FamilyName[-1],element=element)
                self.util.sleep(7)
                self.selectTheSuggResult(FamilyName, locator=self._F_C_ANameSuggList, locatorType="xpath")



    def enterClientName(self,ClientName):
        self.util.sleep(4)
        # if self.waitForElement(locator=self._clientName, locatorType="xpath") != None:
        self.elementClick(locator=self._clientName, locatorType="xpath")
        self.sendKeysbywords(ClientName, locator=self._clientName, locatorType="xpath")
        self.util.sleep(3)
        self.selectTheSuggResult(ClientName, locator=self._F_C_ANameSuggList, locatorType="xpath")

    def enterAccountName(self,AccountName):
        self.util.sleep(4)
        # if self.waitForElement(locator=self._clientName, locatorType="xpath") != None:
        self.elementClick(locator=self._accountname, locatorType="xpath")
        self.sendKeysbywords(AccountName, locator=self._accountname, locatorType="xpath")
        self.util.sleep(3)
        self.selectTheSuggResult(AccountName, locator=self._F_C_ANameSuggList, locatorType="xpath")

    def enterSecondaryEmail(self, email):
        self.sendKeysbywords(data=email,locator=self._SecondaryEmail,locatorType="name")

    def clickcancelbtn(self):
        self.elementClick(locator=self._canceltbtn,locatorType="xpath")

    def clickbackbtn(self):
        self.elementClick(locator=self._backbtn,locatorType="xpath")

    def clicknextbtn(self):
        self.util.sleep(3)
        self.elementClick(locator=self._nextbtn,locatorType="xpath")

    def clickaddproductbtn(self):
        if self.waitForElement(locator=self._tablecontent,locatorType="xpath") != None:
            self.util.sleep(10)
            self.elementClick(locator=self._addproduct,locatorType="name")
        else:
            self.util.sleep(10)
            self.elementClick(locator=self._addproduct, locatorType="name")

    def selectAmc(self,AMCName):
        if self.elementPresenceCheck(locator=self._AMCnamw,byType="xpath") == True:
            self.sendKeysbywords(AMCName,locator=self._AMCnamw,locatorType="xpath")
            self.util.sleep(1)
            self.selectTheSuggResult(AMCName,locator=self._AMCSearchResult,locatorType="xpath")
    #TATA ARBITRAGE FUND - REGULAR - PLAN GROWTH
    def selectScheme(self,schemeName):
        if self.elementPresenceCheck(locator=self._SchmeName,byType="xpath") == True:
            self.sendKeysbywords(schemeName,locator=self._SchmeName,locatorType="xpath")
            self.util.sleep(1)
            self.selectTheSuggResult(schemeName,locator=self._AMCSearchResult,locatorType="xpath")

    def selectHoldingType(self,HoldingType):
        self.selectDropdwon(HoldingType,locator=self._HoldingType,locatorType="xpath")
        self.util.sleep(1)

    def selectFolio(self,Folio):
        self.selectDropdwon(Folio, locator=self._Folio, locatorType="xpath")
        self.util.sleep(1)

    def enterAmount(self,Amount):
        self.sendKeys(Amount,locator=self._Amount,locatorType="xpath")
        self.util.sleep(1)

    def selectExecutionChannel(self,ExeChannel):
        self.selectDropdwon(ExeChannel,locator=self._executionChannel,locatorType="xpath")
        self.util.sleep(1)

    def clickSavebtn(self):
        self.elementClick(locator=self._SaveButton,locatorType="xpath")
        self.util.sleep(7)

    def selectClientConsent(self,ClientConsent):
        self.selectDropdwon(ClientConsent,locator=self._clientConsent,locatorType="xpath")
        self.util.sleep(2)

    def clientConsentAttachment(self,consentpath):
        self.sendKeys(consentpath,locator=self._ClientConsentAttachment,locatorType="xpath")
        self.util.sleep(2)

    def clientEmailId(self,EmailId):
        self.sendKeys(EmailId,locator=self._ClientEmailID,locatorType="xpath")
        self.util.sleep(2)


    def clicksubmitbtn(self):
        self.util.sleep(3)
        self.elementClick(locator=self._submitButton,locatorType="xpath")
        self.util.sleep(7)


    def checkSchemeName(self,schemename):
        self.util.sleep(7)
        result = self.resultList(schemename, locator=self._resultpagelist, locatorType='xpath', i=6)
        self.util.sleep(5)

        return result

    def checkOrderAmount(self,Amount):
        self.util.sleep(5)
        result = self.resultList(Amount, locator=self._resultpagelist, locatorType='xpath', i=14)
        self.util.sleep(5)

        return result

    def returnExistingScheme(self,Scheme):
        self.util.sleep(5)
        pass


    def mfsuccessful(self,MatchText,AmountToBeMatch):
        self.util.sleep(7)

        result = False
        # SN = "//div[@class='slds-form-element__control']/span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11 is-read-only']/slot[@name='outputField']/lightning-formatted-text[@slot='outputField']"
        # AM = "//lightning-formatted-text[@slot='outputField' and text() = "+AmountToBeMatch+"]"
        # schemetext = self.getText(locator=SN, locatorType="xpath")
        # schemetxnAmount = self.getText(locator=AM, locatorType="xpath")
        result1 = self.resultList(MatchText,locator=self._resultpagelist,locatorType='xpath', i = 6)
        self.util.sleep(5)
        # result2 = self.resultList("12340",locator=_resultpagelist,locatorType='xpath',i = 14)
        # self.util.sleep(5)
        self.log.debug("############After finding element text, :: " + str(result1))
        # if result1 and result2 == True:
        #     result = True
        # # else:
        # #     result = False
        # self.log.debug("this is the result of TC "+ result)
        return result1

    def mfFail(self):
        self.util.sleep(2)
        LT = "//*[@id='modal-content-id-1']/div[3]/div/table/tr/td/div/div/table/tbody/tr[1]/td[2]/div"

        text = self.getText(locator=LT, locatorType="xpath")
        if text == "TATA ARBITRAGE FUND - REGULAR - PLAN GROWTHTHTHT":
            result = True
        else:
            result = False

        return result

    def selectTxnType(self,scheme_name):
        rowlist = self.getElementList(locator="//table/tbody/tr",locatorType="xpath")
        for rowindex in range(len(rowlist)):
            self.log.info(rowindex)
            _schemename = "//table/tbody/tr/td["+rowindex+"]/div"
            schemename = self.getText(locator=_schemename,locatorType='xpath')
            self.log.info(schemename)
            if schemename == scheme_name:
                select_locator = "//table/tbody/tr/td["+rowindex+"]/div/div/div/div/select"
                self.selectDropdwon(SelectText='Purchase',locator=select_locator,locatorType='xpath')
                print("value selected ")
                self.log.info("value selected... ")

        self.util.sleep(15)


    def getTxnId(self):
        txnid = self.getText(locator=self._TxnID,locatorType="xpath",info="Transaction Id")
        configParser = configparser.RawConfigParser()
        configFilePath = r'configfiles/project_configuration.config'

        configParser.read(configFilePath)
        configParser['EmailData']['txnid'] = str(txnid)
        with open(configFilePath, 'w') as configfile:
            configParser.write(configfile)

    def addNewTxn(self,AMC, Scheme, HoldingType, Folio, Amount, ExecutionChannel, Remarks):
        pass

    def mfAdditionalPurchase(self,SearchText,FamilyName,ClientName,AccountName,email,SchemeName):
        self.nineDotclick()
        self.searchresult(SearchText)
        self.clickBoldResult()
        self.clickmfLink()
        self.enterFamilyName(FamilyName)
        self.enterClientName(ClientName)
        self.enterAccountName(AccountName)
        self.enterSecondaryEmail(email)
        self.clicknextbtn()
        self.selectTxnType('FRANKLIN INDIA PRIMA FUND-GROWTH')



    def mfFreshPurchase(self, SearchText, FamilyName, ClientName, AccountName, email,AMCName,SchemeName,
                        ClientConsent,consentpath,HoldingType = 'Physical', Folio= 'New',
              OrderAmount = '0', ExecutionChannel = 'POA - Online'):
        self.log.info("MF fresh Order placement start ###############")
        self.nineDotclick()
        self.searchresult(SearchText)
        self.clickBoldResult()
        self.clickmfLink()
        self.enterFamilyName(FamilyName)
        self.enterClientName(ClientName)
        self.enterAccountName(AccountName)
        self.enterSecondaryEmail(email)

        self.clicknextbtn()
        self.clickaddproductbtn()
        self.selectAmc(AMCName)
        self.selectScheme(SchemeName)
        self.selectHoldingType(HoldingType)
        self.selectFolio(Folio)
        self.enterAmount(OrderAmount)
        self.selectExecutionChannel(ExecutionChannel)
        self.clickSavebtn()
        self.clicknextbtn()
        self.selectClientConsent(ClientConsent)
        self.clientConsentAttachment(consentpath)
        self.clientEmailId(email)
        self.clicksubmitbtn()
        self.getTxnId()