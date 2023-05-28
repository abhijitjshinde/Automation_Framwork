from pages.product_creation.mf_txn_page import MfTransaction
from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
import unittest
import pytest
from ddt import ddt,data,unpack
from utilities.read_csv import getCSVData

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class MfTxnTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.mfp = MfTransaction(self.driver)
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=1)
    @data(*getCSVData('MF_Orders.csv'))
    @unpack
    def test_validMfTxn(self,FamilyName,ClientName,AccountName,email,AMCName,SchemeName,HoldingType,Folio,OrderAmount,ExecutionChannel,ClientConsent,Consentpath,AmountToBeMatch):
        self.mfp.mfFreshPurchase(SearchText="Transactions", FamilyName=FamilyName, ClientName=ClientName,
                       AccountName=AccountName, email=email, AMCName=AMCName,
                       SchemeName=SchemeName, HoldingType=HoldingType, Folio=Folio,
                       OrderAmount=OrderAmount, ExecutionChannel=ExecutionChannel,ClientConsent=ClientConsent,consentpath=Consentpath)
        SchemeNameResult = self.mfp.checkSchemeName(SchemeName)
        self.ts.mark(SchemeNameResult,"Order SchemeName is successfully matching")
        OrderAmountResult = self.mfp.checkOrderAmount(AmountToBeMatch)
        self.ts.markFinal("test_validLogin ", OrderAmountResult, "Order placement amount match successfully")
        self.mfp.clickcancelbtn()
        # self.lp.logout()

    @pytest.mark.run(order=2)
    @data(*getCSVData('MF_Orders.csv'))
    @unpack
    def test_invalidMfTxn(self,FamilyName,ClientName,AccountName,email,AMCName,SchemeName,HoldingType,Folio,OrderAmount,ExecutionChannel,ClientConsent,Consentpath,AmountToBeMatch):
        self.mfp.mfFreshPurchase(SearchText="Transactions", FamilyName=FamilyName, ClientName=ClientName,
                                 AccountName=AccountName, email=email, AMCName=AMCName,
                                 SchemeName=SchemeName, HoldingType=HoldingType, Folio=Folio,
                                 OrderAmount=OrderAmount, ExecutionChannel=ExecutionChannel,
                                 ClientConsent=ClientConsent, consentpath=Consentpath)
        result = self.mfp.mfFail()
        self.ts.markFinal("test_validLogin ", result, "Login was successful")
        self.mfp.clickcancelbtn()

    @pytest.mark.run(order=3)
    def test_mfAdditionalPurchase(self):
        self.mfp.mfAdditionalPurchase(SearchText="Transactions", FamilyName="Family - 5102", ClientName="Client - 13142",
                       AccountName="Account - 12138",
                       email="abhijit.shinde@ewmwealth.in",
                       SchemeName="FRANKLIN INDIA PRIMA FUND-GROWTH")
        result = self.mfp.mfFail()
        self.ts.markFinal("test_validLogin ", result, "Login was successful")
        self.mfp.clickcancelbtn()