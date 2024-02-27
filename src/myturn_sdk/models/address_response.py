from .response_base import ResponseBase


class AddressResponse(ResponseBase):
    address: list[str] = None
