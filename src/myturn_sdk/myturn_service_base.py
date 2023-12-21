from .myturn_authenticator import MyTurnAuthenticator
from .browser import Browser


class _MyTurnServiceBase():
    browser: Browser
    libraryUrl: str
    authenticator: MyTurnAuthenticator

    def __init__(self, libraryUrl: str, browser: Browser, authenticator: MyTurnAuthenticator):
        self.libraryUrl = libraryUrl
        self.browser = browser
        self.authenticator = authenticator

    def checklogin(func):
        def wrapper(self, *args):
            self.authenticator.authenticate()
            val = func(self, *args)
            return val
        return wrapper
