import socketio

from app.di.containers import Application
from app.v1.namespace import NameSpaceV1
from config import RedisSettings
from config import ServicesSettings
from misc import sio


def application():
    application_di = Application()
    application_di.gateways.container.config.from_pydantic(RedisSettings())
    application_di.services.container.config.from_pydantic(ServicesSettings())
    application_di.core.init_resources()
    application_di.wire(modules=[__name__])

    app1 = socketio.ASGIApp(sio)
    sio.register_namespace(NameSpaceV1("/v1"))
    return app1


app = application()
