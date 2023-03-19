from dependency_injector import containers
from dependency_injector import providers

from app.di.redis import get_arq_redis
from app.di.redis import get_redis_settings
from app.services.core.client import BackendCoreClient
from app.v1.security.auth import Security


class Core(containers.DeclarativeContainer):

    config = providers.Configuration()


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()

    redis_settings = providers.Singleton(
        get_redis_settings,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        database=config.REDIS_DATABASE,
        password=config.REDIS_PWD,
    )


class Services(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    arq = providers.Factory(
        get_arq_redis,
        settings=gateways.redis_settings,
    )
    security = providers.Factory(
        Security,
        base_url=config.AUTH,
    )

    core = providers.Factory(
        BackendCoreClient,
        base_url=config.CORE,
    )


class Application(containers.DeclarativeContainer):

    config = providers.Configuration()

    core = providers.Container(
        Core,
        config=config.core,
    )

    gateways = providers.Container(
        Gateways,
        config=config.gateways,
    )

    services = providers.Container(
        Services,
        config=config.services,
        gateways=gateways,
    )
