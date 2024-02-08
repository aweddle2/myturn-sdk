from datetime import datetime, timedelta
from .browser import Browser
from .models.login_result import LoginResult


class MyTurnAuthenticator():
    _authUrl: str
    _logoutUrl: str
    # A URL accessible by all users to check if the browser is logged in
    _loggedInUrl: str
    _username: str
    _password: str
    _loginExpiry: datetime = None

    browser: Browser

    def __init__(self, libraryUrl: str, browser: Browser, username: str, password: str):
        self._authUrl = libraryUrl + 'login/auth'
        self._logoutUrl = libraryUrl + 'logout/index'
        self._loggedInUrl = libraryUrl + 'myAccount/index'
        self._username = username
        self._password = password
        self.browser = browser

    def authenticate(self):
        result = self._isUserLoggedIn()

        # If we get a result from the cookie, then return as we are all good
        if (result.success):
            return result

        # If we get here there was no login
        self.browser.get(self._authUrl)
        id_box = self.browser.find_element_by_name('j_username')
        id_box.send_keys(self._username)
        pass_box = self.browser.find_element_by_name('j_password')
        pass_box.send_keys(self._password)
        self.browser.find_element_by_xpath(
            "//input[@name='_spring_security_remember_me']").click()
        self.browser.find_element_by_css_selector(".btn-success").click()

        loginFailedElement = self.browser.find_element_by_xpath(
            "//form[@id='login-form']//div[@class='alert alert-danger ']")  # There is a trailing space at the end of the class name here

        if (loginFailedElement is None):
            result = self._isUserLoggedIn()
        else:
            result.message = loginFailedElement.text

        return result

    def logout(self):
        self._loginExpiry = None
        self.browser.get(self._logoutUrl)

    def _isUserLoggedIn(self):
        result = LoginResult()

        # Check to see if there is an expiry date for the login already
        if (self._loginExpiry != None and self._loginExpiry > datetime.now()):
            result.success = True
            result.expiryDate = self._loginExpiry
            return result

        # Check to see if the user clicked the 'remember' checkbox which creates the 'grails_remember_me' cookie in spring.
        cookies = self.browser.get_cookies()
        for cookie in cookies:
            if cookie.get('name') == 'grails_remember_me':
                exp = datetime.fromtimestamp(cookie.get('expiry'))
                if exp > datetime.now():
                    self._loginExpiry = exp
                    result.success = True
                    result.expiryDate = self._loginExpiry
                    return result

        # Now we check a URL that can only be accessed when logged in to see if they logged in without the 'remember' button
        self.browser.get(self._loggedInUrl)
        # If we've been redirected to the auth page then we are not logged in
        if (self.browser._webdriver.current_url == self._authUrl):
            result.success = False
        else:
            self._loginExpiry = datetime.now() + timedelta(minutes=5)
            result.success = True
            result.expiryDate = self._loginExpiry

        # Return the result
        return result
