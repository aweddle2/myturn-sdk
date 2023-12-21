from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import time
import sys
from seleniumrequests import Chrome

# Fixed to Chrome just now, but there this could be refactored to support any Selenium Browser


class Browser():
    _scriptdir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    _webdriver: webdriver

    def __init__(self):
        self._browserOpen()

    def _browserOpen(self):
        # Options to make headless Chrome work in a Docker container and allow downloading of files for script
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument("--log-level=3")  # fatal
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self._scriptdir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        # create browser instance
        self._webdriver = Chrome(options=chrome_options)
        # function to handle setting up headless download
        self.__enable_download_headless()
        return

    # all: function to enable autodownloading to script directory
    def __enable_download_headless(self):
        self._webdriver.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {
            'behavior': 'allow', 'downloadPath': self._scriptdir}}
        self._webdriver.execute("send_command", params)
        return

    def getAndOpenFile(self, url: str, filename: str):
        # get the file
        self.get(url)
        # wait for file to finish downloading
        while not os.path.exists(self._scriptdir+os.sep+filename) or os.path.exists(self._scriptdir+os.sep+filename+'.crdownload'):
            time.sleep(1)
        # return the open file
        return open(self._scriptdir+os.sep+filename, encoding="utf8")

    def deleteDownload(self, filename: str):
        if os.path.exists(self._scriptdir+os.sep+filename):
            os.remove(self._scriptdir+os.sep+filename)

    def get(self, url: str):
        return self._webdriver.get(url)

    def post(self, url: str, postParams):
        return self._webdriver.request('POST', url, data=postParams)

    def _find_element(self, by, search):
        try:
            element = self._webdriver.find_element(by, search)
            if (element != None):
                return element
            self._wait_for_element_visible(by, search)
            return self._webdriver.find_element(by, search)
        except NoSuchElementException:
            return None

    def find_element_by_css_selector(self, search):
        return self._find_element(By.CSS_SELECTOR, search)

    def find_element_by_xpath(self, search):
        return self._find_element(By.XPATH, search)

    def find_element_by_name(self, search):
        return self._find_element(By.NAME, search)

    def find_element_by_link_text(self, search):
        return self._find_element(By.LINK_TEXT, search)

    def _wait_for_element_visible(self, by, search):
        WebDriverWait(self._webdriver, 30).until(
            EC.visibility_of_element_located(
                (by, search))
        )

    def wait_for_element_visible_by_css_selector(self, search):
        self._wait_for_element_visible(By.CSS_SELECTOR, search)

    def _wait_for_element_clickable(self, by, search):
        WebDriverWait(self._webdriver, 30).until(
            EC.element_to_be_clickable(
                (by, search))
        )

    def get_cookies(self):
        return self._webdriver.get_cookies()

    def add_cookie(self, cookie):
        return self._webdriver.add_cookie(cookie)

    def clickByCssSelector(self, cssElement):
        self._wait_for_element_clickable(By.CSS_SELECTOR, cssElement)
        self.find_element_by_css_selector(cssElement).click()

    def clickByXPath(self, xpath):
        self._wait_for_element_clickable(By.XPATH, xpath)
        self.find_element_by_xpath(xpath).click()

    def setTextByCssElement(self, cssElement, text):
        element = self.find_element_by_css_selector(cssElement)
        element.clear()
        element.send_keys(text)

    def setTextByName(self, name, text):
        element = self.find_element_by_name(name)
        element.clear()
        element.send_keys(text)

    def setSelectByVisibleText(self, name, text):
        element = self.find_element_by_name(name)
        dropdown = Select(element)
        dropdown.select_by_visible_text(text)

    def appendText(self, cssElement, text):
        self.find_element_by_css_selector(cssElement).send_keys(text)
