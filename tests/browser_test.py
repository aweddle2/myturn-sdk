
import unittest
from src.myturn_sdk.browser import Browser
import os
import datetime
from parameterized import parameterized
from seleniumrequests import Chrome
from selenium import webdriver


class BrowserTests(unittest.TestCase):

    def testGET(self):
        # Arrange
        browser = Browser()

        # Act
        browser.get('https://httpbin.org/get')
        # Assert

    def testPOST(self):

        # Arrange
        browser = Browser()

        # Act
        browser.post('https://httpbin.org/post')
        # Assert
