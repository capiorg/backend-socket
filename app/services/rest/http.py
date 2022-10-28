from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from urllib.parse import unquote

import aiohttp
import json
from aiohttp import ContentTypeError

from app.services.rest.exceptions import FailedDecodeJson


class HTTPClient:
    async def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Tuple[Dict[str, Any], int]:

        if not headers:
            headers = {}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method=method, url=url, **kwargs) as resp:
                return await self.__generate_json_from_response(resp)

    async def __generate_json_from_response(
        self, resp: aiohttp.ClientResponse
    ) -> Tuple[Dict[str, Any], int]:
        content_type = resp.headers.get("Content-Type", "")
        try:
            if content_type.startswith("text/plain"):
                resp_text = await resp.text()
                resp_json = json.loads(resp_text)
                return self.__decode_json(resp_json), resp.status

            elif content_type.startswith("application/json"):
                resp_json = await resp.json()
                return resp_json, resp.status
            else:
                raise Exception(
                    "Content type not support [text/plain, application/json]"
                )
        except ContentTypeError as e:
            raise FailedDecodeJson(f"Check args, URL is invalid - {e}")

    @staticmethod
    def __decode_json(data: Union[List, Dict[str, Any]]):
        data_dumps = json.dumps(data, ensure_ascii=False)
        decoded_data_str = unquote(data_dumps)
        data_data_json = json.loads(decoded_data_str)
        return data_data_json
