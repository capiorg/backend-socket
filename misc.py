import socketio

from config import redis_settings

mgr = socketio.AsyncRedisManager(
    redis_settings.dsn,
    channel="sio123"
)
sio = socketio.AsyncServer(
    client_manager=mgr,
    cors_allowed_origins="*",
    async_mode="asgi"
)
