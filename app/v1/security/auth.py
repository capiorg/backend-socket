from app.services.rest.http import HTTPClient
from app.v1.models.http_response import BaseResponse
from app.v1.security.exceptions import UnauthorizedError
from app.v1.security.models import GetUserModel
from app.v1.security.urls import AuthServiceURL


class Security(HTTPClient):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def decode(self, token: str) -> BaseResponse[GetUserModel]:
        prepare_url = f"{self.base_url}{AuthServiceURL.ME}"
        headers = {"Authorization": token}

        response, code = await self._request(
            method="GET",
            url=prepare_url,
            headers=headers
        )
        if code != 200:
            raise UnauthorizedError

        model = BaseResponse[GetUserModel].parse_obj(response)
        model.result.jwt = token
        return model

    async def activity(
        self,
        token: str,
        is_online: bool,
        last_activity: str,

    ):
        url = f"{self.base_url}/api/v1/auth/me/activity"
        headers = {"Authorization": token}

        response, code = await self._request(
            "PATCH",
            url=url,
            json={"is_online": is_online, "last_activity": last_activity},
            headers=headers,
        )
        return response
