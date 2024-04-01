import unittest
from src.myturn_sdk.models.inventory_search_request import InventorySearchRequest, ExportFields
from src.myturn_sdk.myturn_client import MyTurnClient
import os


class MyTurnInventoryIntegrationTests(unittest.TestCase):
    _myTurnClient: MyTurnClient

    @classmethod
    def setUpClass(self):
        myturnSubdomain = os.environ['myturnSubdomain']
        myTurnUsername = os.environ['myturnUsername']
        myturnPassword = os.environ['myturnPassword']

        self._myTurnClient = MyTurnClient(
            myturnSubdomain, myTurnUsername, myturnPassword)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def testExportInventory(self):
        # Arrange
        request = InventorySearchRequest()
        request.exportFields.append(ExportFields.Name)
        request.exportFields.append(ExportFields.Statuses)

        # Act
        response = self._myTurnClient.inventory.inventoryExport(request)

        # Assert
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.inventoryItems)
        self.assertNotEquals(0, len(response.inventoryItems))


if __name__ == '__main__':
    unittest.main()
