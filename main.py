import socketio
import uvicorn as uvicorn

from app.di.containers import Application
from app.v1.namespace import NameSpaceV1
from config import RedisSettings
from config import SecuritySettings
from misc import sio


def application():
    application_di = Application()
    application_di.gateways.container.config.from_pydantic(RedisSettings())
    application_di.services.container.config.from_pydantic(SecuritySettings())
    application_di.core.init_resources()
    application_di.wire(modules=[__name__])

    sio.register_namespace(NameSpaceV1("/v1"))
    return socketio.ASGIApp(sio)


app = application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10100, reload=True, workers=4)
