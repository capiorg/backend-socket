class BaseTokenError(Exception):
    def __init__(self, message: str):
        self.message = message


class ExpireTokenError(BaseTokenError):
    pass


class TokenSubError(BaseTokenError):
    pass


class TokenJWTError(BaseTokenError):
    pass
