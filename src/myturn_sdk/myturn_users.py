from typing import List

from .myturn_authenticated_base import _MyTurnAuthenticatedBase
from .browser import Browser
from .models.user import User
import csv
import time
import datetime


class MyTurnUsers(_MyTurnAuthenticatedBase):
    _userExportToCsvUrl = ''
    _userSearchUrl = ''
    _editUserUrl = ''
    _deleteUserUrl = ''

    # Path to store the cookies file for automated login
    # _mcookies_file = _scriptdir + 'creds' + os.sep + 'mcookies.pkl'

    # Default Constructor.  Logs into MyTurn
    def __init__(self, libraryUrl: str, browser: Browser, username: str, password: str):
        self._userExportToCsvUrl = libraryUrl + 'orgMembership/exportUsers'
        self._userSearchUrl = libraryUrl + 'orgMembership/searchUsers?load=true&keyword='
        self._editUserUrl = libraryUrl + 'orgMembership/editUser?userId='
        self._deleteUserUrl = libraryUrl + 'orgMembership/deleteUser?user.id='
        self._userDetailsUrl = libraryUrl + 'orgMembership/userDetails?userId='
        _MyTurnAuthenticatedBase.__init__(
            self, libraryUrl, browser, username, password)

    @_MyTurnAuthenticatedBase.checklogin
    def getUser(self, userId):
        try:
            userDetailsUrl = self._userDetailsUrl + str(userId)
            self.browser.get(userDetailsUrl)

            u = User()
            u.userId = userId
            u.name = self.browser.find_element_by_xpath(
                "//label[.='Name']/following-sibling::div/div").get_attribute('innerText').replace(u'\xa0', u' ')
            u.email = self.browser.find_element_by_xpath(
                "//label[.='Email']/following-sibling::div/div/a").get_attribute('innerText')
            u.username = self.browser.find_element_by_xpath(
                "//label[.='Username']/following-sibling::div/div").get_attribute('innerText')
            u.phone = self.browser.find_element_by_xpath(
                "//label[.='Phone']/following-sibling::div/div").get_attribute('innerText')
            u.membershipId = int(self.browser.find_element_by_xpath(
                "//label[.='Membership ID']/following-sibling::div/div").get_attribute('innerText'))
            # Membership type contains a sub element for the membership state, so we need to remove that
            membershipState = self.browser.find_element_by_xpath(
                "//label[.='Membership Type']/following-sibling::div/div/span").get_attribute('innerText')
            membershipType = self.browser.find_element_by_xpath(
                "//label[.='Membership Type']/following-sibling::div/div").get_attribute('innerText')
            u.currentMembershipType = membershipType.replace(
                membershipState, '').strip()
            memberCreatedAsString = self.browser.find_element_by_xpath(
                "//label[.='Member Created']/following-sibling::div/div").get_attribute('innerText')
            # TODO : Date format probably need refactored out as I am assuming it is set by the country of the person logged in?
            u.memberCreated = datetime.datetime.strptime(
                memberCreatedAsString, '%d/%m/%Y')
            u.paymentMethod = self.browser.find_element_by_xpath(
                "//label[.='Payment method']/following-sibling::div/div").get_attribute('innerText').replace(' Update', '').replace(' Add', '')
            return u
        except:
            return None

    @_MyTurnAuthenticatedBase.checklogin
    def getUserIdForMembershipId(self, membershipId):
        searchUserUrl = self._userSearchUrl + str(membershipId)
        self.browser.get(searchUserUrl)
        url = self.browser.find_element_by_link_text(
            'Edit').get_attribute('href')
        return int(url[-6:])

    @_MyTurnAuthenticatedBase.checklogin
    def getRequestsToJoin(self):
        users: List[User] = list()

        # These POST params can select what fields to download.  This particular URL only downloads the below
        # Customer ID	First Name	Last Name	Email	Username	Member Created (D/MM/YYYY)	Current Membership Type	User Note
        # If you change this POST Params to add or remove fields, please check this method for fields in the csv by their index
        postParams = [('format', 'csv'), ('extension', 'csv'), ('membershipTypeId', '4031'), ('exportField', 'membership.attributes.membershipId'),
                      ('exportField', 'firstName'), ('exportField', 'lastName'),
                      ('exportField', 'emailAddress'), ('exportField', 'username'),
                      ('exportField', 'membership.memberSince'),
                      ('exportField', 'membershipType.name'),
                      ('exportField', 'attributes.latestNote')
                      ]

        # this will download the file to the downloads directory
        result = self.browser.post(
            self._userExportToCsvUrl, postParams).content.decode('UTF-8').splitlines()

        rows = csv.reader(result)
        for row in rows:
            user = User()
            # The order of the CSV is dependant on the order of the order of the fields in the URL above.
            user.membershipId = row[0]
            user.firstName = row[1]
            user.lastName = row[2]
            user.email = row[3]
            user.username = row[4]
            user.memberCreated = row[5]
            user.currentMembershipType = row[6]
            user.userNote = row[7]
            users.append(user)
        return users

    @_MyTurnAuthenticatedBase.checklogin
    def appendNote(self, userId, note):
        # Get the Edit User Page
        editUserUrl = self._editUserUrl+str(userId)
        self.browser.get(editUserUrl)
        # Click the 'Update Note' button
        self.browser.clickByCssSelector('#user-note-btn')
        # Append the note to the modal window
        self.browser.appendText('#user-note-modal-content', note)
        # Save the modal
        self.browser.clickByXPath(
            "//div[@id='user-note-modal']//button[@class='btn btn-primary submit-btn']")
        # Wait 2 seconds for the modal to save before returning
        # There's no clever way to do this other than with a WebDriverWait and the visibility_of_element_located() method.
        # This is just going to timeout after the alloted time anyway, so it's no more efficient than a sleep
        time.sleep(2)

    @_MyTurnAuthenticatedBase.checklogin
    def setNote(self, userId, note):
        # Get the Edit User Page
        editUserUrl = self._editUserUrl+str(userId)
        self.browser.get(editUserUrl)
        # Click the 'Update Note' button
        self.browser.clickByCssSelector('#user-note-btn')
        # Set the note to the modal window
        self.browser.setTextByCssElement('#user-note-modal-content', note)
        # Save the modal
        self.browser.clickByXPath(
            "//div[@id='user-note-modal']//button[@class='btn btn-primary submit-btn']")
        # Wait 2 seconds for the modal to save before returning
        # There's no clever way to do this other than with a WebDriverWait and the visibility_of_element_located() method.
        # This is just going to timeout after the alloted time anyway, so it's no more efficient than a sleep
        time.sleep(2)

    @_MyTurnAuthenticatedBase.checklogin
    def getNote(self, userId):
        # Get the Edit User Page
        editUserUrl = self._editUserUrl+str(userId)
        self.browser.get(editUserUrl)
        # Get the Note
        return self.browser.find_element_by_css_selector('#user-note').get_attribute("innerText")

    @_MyTurnAuthenticatedBase.checklogin
    def deleteUser(self, userId: int):
        # Get the Delete User Page
        deleteUserUrl = self._deleteUserUrl+str(userId)
        self.browser.get(deleteUserUrl)
        # Click the Delete Button
        self.browser.clickByXPath(
            "//button[.='Delete User']")
        # Click the OK on the confirmation modal
        self.browser.clickByXPath(
            "//div[@class='modal-dialog']//button[@class='btn btn-primary']")
