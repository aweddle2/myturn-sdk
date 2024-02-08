from typing import List
from src.myturn_sdk.models.user_search_request import UserSearchRequest
from src.myturn_sdk.models.user_search_response import UserSearchResponse
from .myturn_service_base import _MyTurnServiceBase
from .myturn_authenticator import MyTurnAuthenticator
from .browser import Browser
from .models.user import User
import csv
import time
import datetime


class MyTurnUsers(_MyTurnServiceBase):
    _userExportToCsvUrl = ''
    _userSearchUrl = ''
    _editUserUrl = ''
    _deleteUserUrl = ''

    # Path to store the cookies file for automated login
    # _mcookies_file = _scriptdir + 'creds' + os.sep + 'mcookies.pkl'

    # Default Constructor
    def __init__(self, libraryUrl: str, browser: Browser, authenticator: MyTurnAuthenticator):
        self._userExportToCsvUrl = libraryUrl + 'orgMembership/exportUsers'
        self._userSearchUrl = libraryUrl + 'orgMembership/searchUsers'
        self._editUserUrl = libraryUrl + 'orgMembership/editUser?userId='
        self._deleteUserUrl = libraryUrl + 'orgMembership/deleteUser?user.id='
        self._userDetailsUrl = libraryUrl + 'orgMembership/userDetails?userId='
        _MyTurnServiceBase.__init__(
            self, libraryUrl, browser, authenticator)

    @_MyTurnServiceBase.checklogin
    def searchUsers(self, request: UserSearchRequest):
        try:
            self._searchUsers(request)

            returnValue = UserSearchResponse()

            rows = self.browser.getTableContents('user-list')

            for row in rows:
                u = User()
                u.username = row[0]
                u.membershipId = row[1]
                u.firstName = row[2]
                u.lastName = row[3]
                u.email = row[4]
                # skip organisation
                u.currentMembershipType = row[6]
                # skip expiration
                returnValue.users.append(u)

            return returnValue
        except Exception as inst:
            if __debug__:
                self.browser._webdriver.execute_script(
                    'window.scrollBy(0,350)', '')
                self.browser._webdriver.save_screenshot(
                    'searchUsersException.png')
            raise inst

    @_MyTurnServiceBase.checklogin
    def getUser(self, userId):
        try:
            userDetailsUrl = self._userDetailsUrl + str(userId)
            self.browser.get(userDetailsUrl)

            u = User()
            u.userId = userId

            fullName = self.browser.getTextByXPath(
                "//h3[.='Personal Info']/parent::div/parent::div//label[.='Name']/following-sibling::div/div")
            # the &nbsp; is always there between the first name and surname, so this should always split successfully into 2 parts.
            nameParts = fullName.split(u'\xa0')
            u.firstName = nameParts[0]
            u.lastName = nameParts[1]
            u.email = self.browser.getTextByXPath(
                "//h3[.='Personal Info']/parent::div/parent::div//label[.='Email']/following-sibling::div/div/a")
            u.phone = self.browser.getTextByXPath(
                "//h3[.='Personal Info']/parent::div/parent::div//label[.='Phone']/following-sibling::div/div")
            u.username = self.browser.getTextByXPath(
                "//label[.='Username']/following-sibling::div/div")
            u.membershipId = int(self.browser.getTextByXPath(
                "//label[.='Membership ID']/following-sibling::div/div"))
            # Membership type contains a sub element for the membership state, so we need to remove that
            membershipState = self.browser.getTextByXPath(
                "//label[.='Membership Type']/following-sibling::div/div/span")
            membershipType = self.browser.getTextByXPath(
                "//label[.='Membership Type']/following-sibling::div/div")
            u.currentMembershipType = membershipType.replace(
                membershipState, '').strip()
            memberCreatedAsString = self.browser.getTextByXPath(
                "//label[.='Member Created']/following-sibling::div/div")
            # TODO : Date format probably need refactored out as I am assuming it is set by the country of the person logged in?
            u.memberCreated = datetime.datetime.strptime(
                memberCreatedAsString, '%d/%m/%Y')
            u.paymentMethod = self.browser.getTextByXPath(
                "//label[.='Payment method']/following-sibling::div/div").replace(' Update', '').replace(' Add', '')
            return u
        except:
            return None

    @_MyTurnServiceBase.checklogin
    def getUserIdForMembershipId(self, membershipId):
        try:
            request = UserSearchRequest()
            request.search = membershipId
            self._searchUsers(request)

            url = self.browser.find_element_by_link_text(
                'Edit').get_attribute('href')
            return int(url[-6:])
        except Exception as inst:
            if __debug__:
                self.browser._webdriver.save_screenshot(
                    'getUserIdForMembershipIdException.png')
            raise inst

    def _searchUsers(self, request: UserSearchRequest):
        # TODO Work out why a delay is needed here!
        time.sleep(2)
        self.browser.get(self._userSearchUrl)
        # Need some time to let some javascript render, but can't find a good way of detecting when it has finished.
        time.sleep(1)
        # Can't search by name here as there are 2 elements with the name 'keyword'
        if (len(request.search) > 0):
            self.browser.setTextByXPath(
                "//form[@id='userSearchParams']//input[@name='keyword']", request.search)

        if (len(request.email) > 0):
            # Click 'Advanced' Tab
            self.browser.clickByID('tab_1_1')
            # sleep until the according expands.  Know this is bad practise, but it is a fixed time in jQuery and the html changes after it has expanded are hard to test for.
            time.sleep(2)
            self.browser.setTextByName('emailAddress', request.email)

        self.browser.clickByCssSelector('.btn-primary')
        # Wait for loading spinner to dissapear
        self.browser.wait_for_element_removed_by_css_selector(
            '.blockUI')

    @_MyTurnServiceBase.checklogin
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
        response = self.browser.post(self._userExportToCsvUrl, postParams)
        result = response.content.decode('UTF-8').splitlines()

        rows = csv.reader(result)
        # skip header
        next(rows)
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

    @_MyTurnServiceBase.checklogin
    def appendNote(self, userId, note):
        # Get the Edit User Page
        editUserUrl = self._editUserUrl+str(userId)
        self.browser.get(editUserUrl)
        # Click the 'Update Note' button
        self.browser.clickByCssSelector('#user-note-btn')
        # Wait for the modal to open
        self.browser.wait_for_element_visible_by_css_selector(
            '#user-note-modal-content')
        # Append the note to the modal window
        self.browser.appendText('#user-note-modal-content', note)
        # Save the modal
        self.browser.clickByXPath(
            "//div[@id='user-note-modal']//button[@class='btn btn-primary submit-btn']")
        self.browser.wait_for_element_invisible_by_css_selector(
            '#user-note-modal')

    @_MyTurnServiceBase.checklogin
    def setNote(self, userId, note):
        # Get the Edit User Page
        editUserUrl = self._editUserUrl+str(userId)
        self.browser.get(editUserUrl)
        # Click the 'Update Note' button
        self.browser.clickByCssSelector('#user-note-btn')

        # Wait for the modal to open
        self.browser.wait_for_element_visible_by_css_selector(
            '#user-note-modal-content')

        # Set the note to the modal window
        self.browser.setTextByCssSelector('#user-note-modal-content', note)
        # Save the modal
        self.browser.clickByXPath(
            "//div[@id='user-note-modal']//button[@class='btn btn-primary submit-btn']")

        self.browser.wait_for_element_invisible_by_css_selector(
            '#user-note-modal')

    @_MyTurnServiceBase.checklogin
    def getNote(self, userId):
        # Get the Edit User Page
        editUserUrl = self._editUserUrl+str(userId)
        self.browser.get(editUserUrl)
        # Get the Note
        return self.browser.find_element_by_css_selector('#user-note').get_attribute("innerText")

    @_MyTurnServiceBase.checklogin
    def deleteUser(self, userId: int):
        if userId is None:
            raise ValueError("userId must be specified")

        # Get the Delete User Page
        deleteUserUrl = self._deleteUserUrl+str(userId)
        self.browser.get(deleteUserUrl)
        # Click the Delete Button
        self.browser.clickByXPath(
            "//button[.='Delete User']")
        # Click the OK on the confirmation modal
        self.browser.clickByXPath(
            "//div[@class='modal-dialog']//button[@class='btn btn-primary']")
