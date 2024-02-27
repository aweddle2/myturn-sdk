from .response_base import ResponseBase
from .user import User


class UserSearchResponse(ResponseBase):
    users: list[User] = list()
