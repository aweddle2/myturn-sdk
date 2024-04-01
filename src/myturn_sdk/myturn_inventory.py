from .models.inventory_search_request import InventorySearchRequest
from .models.inventory_search_response import InventorySearchResponse
from .models.inventory_item import InventoryItem
from .myturn_service_base import _MyTurnServiceBase
from .myturn_authenticator import MyTurnAuthenticator
from .browser import Browser
import csv
import os


class MyTurnInventory(_MyTurnServiceBase):
    _inventoryExportUrl = ''

    # Default Constructor
    def __init__(self, libraryUrl: str, browser: Browser, authenticator: MyTurnAuthenticator):
        self._inventoryExportUrl = libraryUrl + 'orgInventory/report'
        _MyTurnServiceBase.__init__(
            self, libraryUrl, browser, authenticator)

    @_MyTurnServiceBase.checklogin
    def inventoryExport(self, request: InventorySearchRequest):

        returnValue = InventorySearchResponse()
        downloadedFileName: str = None
        try:
            # go to inventory export page
            self.browser.get(self._inventoryExportUrl)

            # set the Export Type
            self.browser.clickByXPath(
                "//label[contains(.,'"+request.exportType.value[1]+"')]")
            # set the fields
            for field in request.exportFields:
                xpath = "//label[contains(.,'"+field.value[1]+"')]"
                childSpanWithCheckedClass = self.browser.find_element_by_xpath(
                    xpath+"//span[@class='checked']")
                # if no element was returned then the checkbox is not checked, so check it
                if (childSpanWithCheckedClass is None):
                    self.browser.clickByXPath(xpath)

            # click the csv button
            self.browser.clickByCssSelector('.csv.btn')

            # wait for spinner to dissapear for file to download
            self.browser.wait_for_element_removed_by_css_selector(
                '.loading-message.loading-message-boxed')

            # open the last downloaded file (as we don't know the filename)
            result = self.browser.openLastDownloadedFile()
            # set the downloaded filename so we can delete it even if something goes wrong below
            downloadedFileName = result.name

            rows = csv.reader(result)
            # get header to get field order as these were selected above
            headerRow = next(rows)
            for row in rows:
                item = InventoryItem()
                item.ItemID = row[0]
                if 'Status(es)' in headerRow:
                    item.Statuses = row[headerRow.index(
                        'Status(es)')].split(',')
                if 'Name' in headerRow:
                    item.Name = row[headerRow.index('Name')]
                returnValue.inventoryItems.append(item)

            returnValue.success = True
        except Exception as ex:
            returnValue.message = ex
        finally:
            # delete the download if it exists
            if (downloadedFileName is not None):
                os.remove(downloadedFileName)

        return returnValue
