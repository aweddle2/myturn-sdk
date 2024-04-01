from .browser import Browser
from .myturn_users import MyTurnUsers
from .myturn_my_account import MyTurnMyAccount
from .myturn_public_info import MyTurnPublicInfo
from .myturn_authenticator import MyTurnAuthenticator
from .myturn_inventory import MyTurnInventory


class MyTurnClient():
    users: MyTurnUsers
    myAccount: MyTurnMyAccount
    publicInfo: MyTurnPublicInfo
    inventory: MyTurnInventory

    def __init__(self, myturnSubDomain: str, username: str, password: str, headless: bool = True):
        libraryUrl = 'https://'+myturnSubDomain+'.myturn.com/library/'
        browser = Browser(headless)
        authenticator = MyTurnAuthenticator(
            libraryUrl, browser, username, password)

        self.users = MyTurnUsers(libraryUrl, browser, authenticator)
        self.myAccount = MyTurnMyAccount(libraryUrl, browser, authenticator)
        self.publicInfo = MyTurnPublicInfo(libraryUrl, browser)
        self.inventory = MyTurnInventory(libraryUrl, browser, authenticator)
