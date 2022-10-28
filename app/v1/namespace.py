import datetime
from pprint import pprint
from typing import Any

import socketio
from arq import ArqRedis
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from app.di.containers import Application
from app.utils.encoders import jsonable_encoder
from app.v1.models.http_response import BaseResponse
from app.v1.models.on_typing import TypingPubModel
from app.v1.models.on_typing import TypingSubModel
from app.v1.security.auth import Security
from app.v1.security.exceptions import UnauthorizedError
from app.v1.security.models import GetUserModel
from app.v1.security.models import SmallUserModel


class NameSpaceV1(socketio.AsyncNamespace):

    @inject
    async def on_connect(
        self,
        sid: str,
        data: dict[str, Any],
        security: Security = Provide[Application.services.security],
        arq_client: ArqRedis = Provide[Application.services.arq],
    ):
        auth_jwt_token = data.get("HTTP_AUTH_JWT", None)
        try:
            security_data = await security.decode(token=auth_jwt_token)
            await self.save_session(sid, security_data.dict())
            await self.emit("connected", {"result": True})
            # await arq_client.enqueue_job("update_last_activity", user_uuid=auth["username"])

        except UnauthorizedError:
            await self.disconnect(sid=sid)

    async def on_disconnect(self, sid):
        await self.emit("disconnected", {"result": True})
        await self.disconnect(sid=sid)

    @inject
    async def on_typing(
        self,
        sid,
        data,
        arq_client: ArqRedis = Provide[Application.services.arq],
    ):
        request_data_model = TypingSubModel.parse_obj(data)

        session_dict = await self.get_session(sid)
        session_model = BaseResponse[GetUserModel].parse_obj(session_dict)

        response_model = TypingPubModel(
            author=SmallUserModel.parse_obj(session_model.result),
            conversation_id=request_data_model.conversation_id,
            created_at=datetime.datetime.now(),
        )

        await self.emit(
            "typingResponse",
            jsonable_encoder(response_model.dict()),
            skip_sid=sid
        )
