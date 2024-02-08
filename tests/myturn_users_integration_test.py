import random
import string
import unittest
from src.myturn_sdk.models.user_search_request import UserSearchRequest
from src.myturn_sdk.models.user import User
from src.myturn_sdk.myturn_client import MyTurnClient
import os
import datetime


class MyTurnUsersIntegrationTests(unittest.TestCase):
    _membershipId: int
    _userId: int
    _myTurnClient: MyTurnClient
    _user: User

    @classmethod
    def setUpClass(self):
        myturnSubdomain = os.environ['myturnSubdomain']
        myTurnUsername = os.environ['myturnUsername']
        myturnPassword = os.environ['myturnPassword']
        self._membershipId = os.environ['myturnMembershipId']
        self._userId = os.environ['myturnUserId']

        self._myTurnClient = MyTurnClient(
            myturnSubdomain, myTurnUsername, myturnPassword, False)
        self._user = User()
        self._user.firstName = 'Integration'
        self._user.lastName = 'User'
        self._user.address1 = '742 Evergreen Terrace'
        self._user.address2 = 'Random Suburb'
        self._user.city = 'Springfield'
        self._user.country = 'Australia'
        self._user.postalCode = '90210'
        self._user.dateOfBirth = datetime.datetime(1999, 3, 3)
        self._user.email = 'homer@thesimpsons.com'
        self._user.username = 'hsimpson1251956'
        self._user.phone = '0412345678'

    @classmethod
    def tearDownClass(self):
        # Always delete the test user at the end of the run
        request = UserSearchRequest()
        request.email = self._user.email
        response = self._myTurnClient.users.searchUsers(request)

        # If there's a test user, delete it
        if (len(response.users) > 0):
            userId = self._myTurnClient.users.getUserIdForMembershipId(
                response.users[0].membershipId)
            self._myTurnClient.users.deleteUser(userId)

    def setUp(self):
        # Create Test User If Not Exist
        request = UserSearchRequest()
        request.email = self._user.email
        response = self._myTurnClient.users.searchUsers(request)

        # If there's no test user, create it and populate the membership ID and user ID
        if (len(response.users) == 0):
            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for i in range(16))
            self._myTurnClient.myAccount.createUser(self._user, password)
            # When creating a user in the above way, the user is also logged in, so we need to log them out so we can log our admin user back in
            self._myTurnClient.myAccount.logout()
            response = self._myTurnClient.users.searchUsers(request)

        self._user.membershipId = response.users[0].membershipId
        self._user.userId = self._myTurnClient.users.getUserIdForMembershipId(
            self._user.membershipId)

    def testSearchUser(self):
        # Arrange
        request = UserSearchRequest()
        request.email = self._user.email

        # Act
        response = self._myTurnClient.users.searchUsers(request)

        # Assert
        self.assertIsNotNone(response)
        self.assertEqual(self._user.name, response.users[0].name)
        self.assertEqual('New Membership Request',
                         response.users[0].currentMembershipType)
        # self.assertEqual(self._user.userId, self._userId)
        self.assertIsNotNone(response.users[0].membershipId)
        # should not be the membershipid of the logged in user
        self.assertNotEqual(response.users[0].membershipId, self._membershipId)

    # def testSetupAndTearDown(self):
    #     pass

    # def testLogout(self):
    #     self._myTurnClient.myAccount.logout()

    #     self._myTurnClient.users.getNote(self._userId)

    def testGetUserIdForMembershipId(self):
        # Arrange
        # All done in the setUpClass Method

        # Act
        self._user.userId = self._myTurnClient.users.getUserIdForMembershipId(
            self._user.membershipId)

        # Assert
        self.assertIsNotNone(self._user.userId)
        self.assertNotEqual(self._user.userId, self._userId,
                            'User Id should be different from the admin user')

    def testGetRequestsToJoin(self):
        # Arrange
        # All done in the setUpClass Method

        # Act
        users = self._myTurnClient.users.getRequestsToJoin()

        # Assert
        self.assertTrue(len(users) > 0)
        self.assertTrue(
            self._user.firstName in user.firstName for user in users)

    def testAppendNote(self):
        # Arrange
        request = UserSearchRequest()
        request.email = self._user.email
        response = self._myTurnClient.users.searchUsers(request)
        self._user.membershipId = response.users[0].membershipId
        self._user.userId = self._myTurnClient.users.getUserIdForMembershipId(
            self._user.membershipId)

        oldNote = self._myTurnClient.users.getNote(self._user.userId)
        # If the note is empty, MyTurn returns it as a unicode non breaking space, so lets ditch that.
        oldNote = oldNote.replace(u'\xa0', u' ')

        # Act
        self._myTurnClient.users.appendNote(
            self._user.userId, " This is a test Note")

        # Assert
        newNote = self._myTurnClient.users.getNote(self._user.userId)
        # Set the old note back before asserting so it actually runs in case the assert throws an exception
        self._myTurnClient.users.setNote(self._user.userId, oldNote)
        self.assertEqual((oldNote+' This is a test Note').strip(), newNote)

    def testGetUser(self):
        # Arrange

        # Act
        user = self._myTurnClient.users.getUser(self._user.userId)

        # Assert
        self.assertIsNotNone(user)
        self.assertEqual(self._user.name, user.name)
        self.assertEqual('New Membership Request',
                         user.currentMembershipType)
        # self.assertEqual(self._user.userId, self._userId)
        self.assertIsNotNone(user.membershipId)
        # should not be the membershipid of the logged in user
        self.assertNotEqual(user.membershipId, self._membershipId)
        # TODO Other Asserts to go here

    def testGetUserDoesNotExist(self):
        # Arrange

        # Act
        user = self._myTurnClient.users.getUser(999999)

        # Assert
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()
