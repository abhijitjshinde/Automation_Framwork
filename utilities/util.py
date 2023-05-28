"""
@package utilities

Util class implementation
All most commonly used utilities should be implemented in this class

Example:
    name = self.util.getUniqueName()
"""
import time
import traceback
import random, string
import utilities.custom_logger as cl
import logging
import configparser
import requests
from requests.auth import HTTPBasicAuth

class Util(object):

    log = cl.customLogger(logging.INFO)

    def sleep(self, sec, info=""):
        """
        Put the program to wait for the specified amount of time
        """
        if info is not None:
            self.log.info("Wait :: '" + str(sec) + "' seconds for " + info)
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def getAlphaNumeric(self, length, type='letters'):
        """
        Get random string of characters

        Parameters:
            length: Length of string, number of characters string should have
            type: Type of characters string should have. Default is letters
            Provide lower/upper/digits for different types
        """
        alpha_num = ''
        if type == 'lower':
            case = string.ascii_lowercase
        elif type == 'upper':
            case = string.ascii_uppercase
        elif type == 'digits':
            case = string.digits
        elif type == 'mix':
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    def getUniqueName(self, charCount=10):
        """
        Get a unique name
        """
        return self.getAlphaNumeric(charCount, 'lower')

    def getUniqueNameList(self, listSize=5, itemLength=None):
        """
        Get a list of valid email ids

        Parameters:
            listSize: Number of names. Default is 5 names in a list
            itemLength: It should be a list containing number of items equal to the listSize
                        This determines the length of the each item in the list -> [1, 2, 3, 4, 5]
        """
        nameList = []
        for i in range(0, listSize):
            nameList.append(self.getUniqueName(itemLength[i]))
        return nameList

    def verifyTextContains(self, actualText, expectedText):
        """
        Verify actual text contains expected text string

        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### VERIFICATION CONTAINS !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT CONTAINS !!!")
            return False

    def verifyTextMatch(self, actualText, expectedText):
        """
        Verify text match

        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if actualText.lower() == expectedText.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT MATCHED !!!")
            return False

    def verifyListMatch(self, expectedList, actualList):
        """
        Verify two list matches

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        return set(expectedList) == set(actualList)

    def verifyListContains(self, expectedList, actualList):
        """
        Verify actual list contains elements of expected list

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
        else:
            return True

    def getConfig(self,section,item):
        configParser = configparser.RawConfigParser()
        configFilePath = r'configfiles/project_configuration.config'
        configParser.read(configFilePath)
        result = configParser[section][item]
        return result
    def clearTxnId(self):
        configParser = configparser.RawConfigParser()
        configFilePath = r'configfiles/project_configuration.config'
        configParser.read(configFilePath)
        configParser['EmailData']['txnid'] = ''
        with open(configFilePath, 'w') as configfile:
            configParser.write(configfile)
    def sendEmail(self,tc_result):
        """
        use to send email
        """
        TxnId = self.getConfig('EmailData', 'txnid')
        To_Email = self.getConfig('EmailData','to')
        From = self.getConfig('EmailData','from')
        subject = self.getConfig('EmailData','subject')
        if tc_result == True :
            body =TxnId+" "+ self.getConfig('EmailData','body')
        else:
            body = "Purchase order has been Failed. please refer failed screenshot in below path"
        API = self.getConfig('EmailConf','emailapi')
        username = self.getConfig('EmailConf','apiusername')
        password = self.getConfig('EmailConf','apipassword')
        CC = self.getConfig('EmailData','cc')
        data = {
            "Subject": subject,
            "Body": body,
            "TO": To_Email,
            "MailFrom": From,
            "CC": CC,
            "BCC": ""
        }

        r = requests.post(url=API, data=data, auth=HTTPBasicAuth(username, password))
        self.clearTxnId()
        # extracting response text
        pastebin_url = r.text
        print("Mail has been sent ##########")
        print("The pastebin URL is:%s" % pastebin_url)