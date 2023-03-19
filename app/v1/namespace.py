import datetime
from typing import Any

from arq import ArqRedis
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from socketio import AsyncNamespace

from app.di.containers import Application
from app.utils.encoders import jsonable_encoder
from app.utils.redis import AsyncNameSpaceUtils
from app.v1.models.on_typing import TypingPubModel
from app.v1.models.on_typing import TypingSubModel
from app.v1.security.auth import Security
from app.v1.security.exceptions import UnauthorizedError
from app.v1.security.models import SmallUserModel
from urllib import parse


class NameSpaceV1(AsyncNameSpaceUtils, AsyncNamespace):

    @inject
    async def on_connect(
        self,
        sid: str,
        data: dict[str, Any],
    ):
        query_string = data.get("QUERY_STRING")
        parsed_query = parse.parse_qs(query_string)
        auth_jwt_token = parsed_query.get("jwt", [])
        if auth_jwt_token:

            try:
                await self.session_save(sid=sid, jwt_token=auth_jwt_token[0])
                await self.emit("connected", {"result": True})

            except UnauthorizedError:
                await self.on_disconnect(sid=sid)
        else:
            await self.on_disconnect(sid=sid)

    async def on_disconnect(self, sid):

        await self.session_close(sid=sid)
        await self.disconnect(sid=sid)

    async def on_typing(
        self,
        sid,
        data,
    ):
        me = await self.session_me(sid=sid)

        request_data_model = TypingSubModel.parse_obj(data)

        response_model = TypingPubModel(
            author=SmallUserModel.parse_obj(me),
            conversation_id=request_data_model.conversation_id,
            created_at=datetime.datetime.now(),
        )

        await self.emit(
            "typingResponse",
            jsonable_encoder(response_model.dict()),
            skip_sid=sid
        )
