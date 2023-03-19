import socketio

from config import redis_settings

mgr = socketio.AsyncRedisManager(
    redis_settings.dsn,
    channel=redis_settings.REDIS_DB_QUEUE_CHANNEL,
)

sio = socketio.AsyncServer(
    client_manager=mgr,
    cors_allowed_origins="*",
    cors_credentials=True,
    async_mode="asgi"
)
