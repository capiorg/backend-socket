import datetime

from jose import JWTError
from jose import jwt

from app.v1.security.exceptions import ExpireTokenError
from app.v1.security.exceptions import TokenJWTError
from app.v1.security.exceptions import TokenSubError
from app.v1.security.models import TokenSessionModel


def remove_token_type_in_token(token: str):
    if token.lower().startswith("bearer"):
        token = token.replace("Bearer ", "")
    return token


class Security:
    def __init__(self, jwt_secret: str, jwt_algorithm: str):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    def decode(self, token: str) -> TokenSessionModel:
        reformat_token = remove_token_type_in_token(token)

        try:
            payload = jwt.decode(
                reformat_token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
                options={"verify_aud": False},
            )
            sub = payload.get("sub", None)
            session = payload.get("session", None)

            if datetime.datetime.now().timestamp() > payload.get("exp"):
                raise ExpireTokenError(message="Время жизни токена истекло")

        except JWTError as exc:
            raise TokenJWTError(message=str(exc))

        if sub is None:
            raise TokenSubError(
                message="Нарушена сигнатура токена. Отсутствует UUID пользователя."
            )

        return TokenSessionModel(uuid=sub, session=session)
