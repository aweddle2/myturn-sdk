from .response_base import ResponseBase
from .inventory_item import InventoryItem


class InventorySearchResponse(ResponseBase):
    inventoryItems: list[InventoryItem] = list()
