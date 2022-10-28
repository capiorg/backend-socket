from enum import Enum


class AuthServiceURL(str, Enum):
    ME = "/api/v1/auth/me"
