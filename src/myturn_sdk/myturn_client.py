from .browser import Browser
from .myturn_users import MyTurnUsers
from .myturn_my_account import MyTurnMyAccount
from .myturn_authenticator import MyTurnAuthenticator


class MyTurnClient():
    users: MyTurnUsers
    myAccount: MyTurnMyAccount

    def __init__(self, myturnSubDomain: str, username: str, password: str, headless: bool = True):
        libraryUrl = 'https://'+myturnSubDomain+'.myturn.com/library/'
        browser = Browser(headless)
        authenticator = MyTurnAuthenticator(
            libraryUrl, browser, username, password)

        self.users = MyTurnUsers(libraryUrl, browser, authenticator)
        self.myAccount = MyTurnMyAccount(libraryUrl, browser, authenticator)
