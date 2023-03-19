import datetime

from app.services.rest.http import HTTPClient


class BackendCoreClient(HTTPClient):

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def activity(
        self,
        token: str,
        is_online: bool,
        last_activity: str,

    ):
        url = f"{self.base_url}/auth/me/activity"
        headers = {"Authorization": token}

        return await self._request(
            "PATCH",
            url=url,
            data={"is_online": is_online, "last_activity": last_activity},
            headers=headers,
        )
