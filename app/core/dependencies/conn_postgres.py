from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from app.helpers.abc_async_engines_singleton import ABCAsyncDBEnginesSingleton

from app.core.config import settings


Base: DeclarativeMeta = declarative_base()


class AsyncDBEngines(metaclass=ABCAsyncDBEnginesSingleton):

    def __init__(self):
        self.gs1_write_engine = None

    def init_engines(self) -> None:
        if self.gs1_write_engine is None:
            self.gs1_write_engine = self._create_engine(
                url=settings.MS.DATABASE_URL,
                pool_size=1,
                max_overflow=1,
                application_name=f"AzFuncQueueTriggerRVCCodes__write__gs1",
            )
        self.__class__.engines = [
            self.gs1_write_engine,
        ]

    def _create_engine(self, url, pool_size, max_overflow, application_name):
        return self.__class__.create_engine(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            application_name=application_name,
        )

    async def check_connection_async(self):
        await self.__class__.check_connection_engines_async()


def get_engines() -> AsyncDBEngines:
    return AsyncDBEngines()
