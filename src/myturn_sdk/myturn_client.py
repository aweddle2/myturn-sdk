from .browser import Browser
from .myturn_users import MyTurnUsers
from .myturn_my_account import MyTurnMyAccount


class MyTurnClient():
    users: MyTurnUsers
    myAccount: MyTurnMyAccount

    def __init__(self, myturnSubDomain: str, username: str, password: str):
        libraryUrl = 'https://'+myturnSubDomain+'.myturn.com/library/'
        browser = Browser()
        self.users = MyTurnUsers(libraryUrl, browser, username, password)
        self.myAccount = MyTurnMyAccount(
            libraryUrl, browser, username, password)
