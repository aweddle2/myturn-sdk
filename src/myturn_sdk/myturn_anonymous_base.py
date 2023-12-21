from .models.login_result import LoginResult
from .browser import Browser


class _MyTurnAnonymousBase():
    browser: Browser
    libraryUrl: str

    def __init__(self, libraryUrl: str, browser: Browser):
        self.libraryUrl = libraryUrl
        self.browser = browser
