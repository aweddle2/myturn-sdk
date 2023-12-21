from datetime import date


class LoginResult():
    success: bool = False
    message: str = ''
    expiryDate: date
