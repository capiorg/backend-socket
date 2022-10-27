from typing import Any

import socketio
from arq import ArqRedis
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from app.di.containers import Application
from app.v1.security.auth import Security
from app.v1.security.exceptions import BaseTokenError


class NameSpaceV1(socketio.AsyncNamespace):

    @inject
    async def on_connect(
        self,
        sid: str,
        data: dict[str, Any],
        auth: dict[str, Any],
        security: Security = Provide[Application.services.security],
        arq_client: ArqRedis = Provide[Application.services.arq],
    ):
        try:
            security_data = security.decode(token=auth.get("jwt"))
            await self.save_session(sid, security_data.dict())
            await self.emit("connected", {"result": True})
            # await arq_client.enqueue_job("update_last_activity", user_uuid=auth["username"])

        except BaseTokenError as exc:
            await self.emit(
                "auth_error",
                {
                    "status": False,
                    "code": "403",
                    "error": {"code": 403, "message": exc.message},
                },
            )
            await self.disconnect(sid=sid)

    async def on_disconnect(self, sid):
        await self.emit("disconnected", {"result": True})
        await self.disconnect(sid=sid)

    @inject
    async def on_my_event(
        self,
        sid,
        data,
        arq_client: ArqRedis = Provide[Application.services.arq],
    ):
        print(f"{arq_client=}")
        print("ЯЙЦА))")
        await self.emit("my_response", data)
        await self.disconnect(sid=sid)
