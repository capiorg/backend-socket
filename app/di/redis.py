from contextlib import asynccontextmanager
from typing import AsyncGenerator

from arq import ArqRedis
from arq import create_pool
from arq.connections import RedisSettings


def get_redis_settings(
    host: str,
    port: int,
    password: str,
    database: int = 3,
):
    return RedisSettings(
        host=host,
        port=port,
        database=database,
        password=password,
    )


@asynccontextmanager
async def get_arq_redis_with_context(
    settings: RedisSettings,
) -> AsyncGenerator[ArqRedis, None]:
    try:
        redis = await create_pool(settings_=settings)
        yield redis
    except Exception as exc:
        print(f"ошибка {exc}")
        print(exc.__class__.__name__)
        raise Exception from exc


async def get_arq_redis(
    settings: RedisSettings,
):
    async with get_arq_redis_with_context(settings=settings) as arq_redis:
        yield arq_redis
