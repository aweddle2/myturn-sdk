from .models.user import User
from .browser import Browser
from .myturn_authenticator import MyTurnAuthenticator
from .myturn_service_base import _MyTurnServiceBase
import time


class MyTurnMyAccount(_MyTurnServiceBase):
    paymentMethodUrl = ''
    selectMembershipTypeUrl = ''
    _publicCreateUserUrl = ''

    def __init__(self, libraryUrl: str, browser: Browser, authenticator: MyTurnAuthenticator):
        self.paymentMethodUrl = libraryUrl + 'myAccount/paymentMethod'
        self.selectMembershipTypeUrl = libraryUrl + 'myAccount/selectMembershipType'
        self.editMembershipUrl = libraryUrl + 'myAccount/editMembership'
        self._publicCreateUserUrl = libraryUrl + 'createUser/create'
        _MyTurnServiceBase.__init__(
            self, libraryUrl, browser, authenticator)

    def createUser(self, user: User, password: str):
        # Get the create user page
        self.browser.get(self._publicCreateUserUrl)
        # Set the properties of the page
        self.browser.setTextByName('firstName', user.firstName)
        self.browser.setTextByName('lastName', user.lastName)
        self.browser.setTextByName('emailAddress', user.email)
        self.browser.setTextByName('username', user.username)
        self.browser.setTextByName('password', password)
        self.browser.setTextByName('password2', password)
        self.browser.setTextByName('address.street1', user.address1)
        self.browser.setTextByName('address.street2', user.address2)
        self.browser.setTextByName('address.city', user.city)
        self.browser.setSelectByVisibleText('address.country', user.country)
        self.browser.setTextByName('address.postalCode', user.postalCode)
        self.browser.setTextByName('address.phone', user.phone)
        # Get the date format for the date of birth
        dobPlaceholder = self.browser.find_element_by_name(
            'dateOfBirth_date').get_attribute('placeholder')
        # Assuming all languages conform to the format 'Date of Birth (m/d/yyyy)'
        dateFormat = dobPlaceholder[dobPlaceholder.index(
            '(')+1: dobPlaceholder.index(')')]

        dateFormat = self._myTurnDateFormatTostrftimeFormat(dateFormat)

        self.browser.setTextByName(
            'dateOfBirth_date', user.dateOfBirth.strftime(dateFormat))

        # check the checkbox
        self.browser.find_element_by_name('hasAcceptedAgreements').click()

        # click the submit button
        self.browser.clickByCssSelector('.btn-success')

        return

    def _myTurnDateFormatTostrftimeFormat(self, myTurnDateFormat: str):
        if (myTurnDateFormat is None):
            return None
        # Replace the format with Python standard strftime formatting
        # sometimes the format in myturn is dd/mm/yyyy and sometimes d/m/yyyy so lets replace the double characters first
        # Lastly these replaces will give 2 % signs, so replace them with a single one
        return myTurnDateFormat.replace('dd', '%d').replace('d', '%d').replace(
            'mm', '%m').replace('m', '%m').replace('yyyy', '%Y').replace('%%', '%')

    def logout(self):
        self.authenticator.logout()
        time.sleep(3)
