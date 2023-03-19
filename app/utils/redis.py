import datetime

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from redis.asyncio.client import Redis
from socketio import AsyncNamespace

from app.di.containers import Application
from app.v1.models.http_response import BaseResponse
from app.v1.security.auth import Security
from app.v1.security.models import GetUserModel


class AsyncNameSpaceUtils(AsyncNamespace):
    @property
    def redis(self) -> Redis:
        return self.server.manager.redis

    async def session_me(self, sid: str) -> GetUserModel:
        session_data = await self.get_session(sid)
        session_model = BaseResponse[GetUserModel].parse_obj(session_data)
        return session_model.result

    @inject
    async def session_save(
        self,
        sid: str,
        jwt_token: str,
        security: Security = Provide[Application.services.security],
    ) -> None:
        security_data = await security.decode(token=jwt_token)
        await self.save_session(sid, security_data.dict())

        await self.redis.rpush(
            f"socketio_user:{security_data.result.uuid}", sid
        )
        await security.activity(
            token=security_data.result.jwt,
            is_online=True,
            last_activity=datetime.datetime.now().isoformat()
        )

    @inject
    async def session_close(
        self,
        sid: str,
        security: Security = Provide[Application.services.security],
    ) -> None:
        me = await self.session_me(sid=sid)

        await self.redis.lrem(
            name=f"socketio_user:{me.uuid}",
            count=0,
            value=sid
        )

        count_sids = await self.redis.llen(f"socketio_user:{me.uuid}")

        if count_sids == 0:
            await security.activity(
                token=me.jwt,
                is_online=False,
                last_activity=datetime.datetime.now().isoformat()
            )
