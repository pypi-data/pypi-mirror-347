from typing import Any, Generic, TypeVar, Union

from nexuslabdata.connection.base.connection import CONNECTION
from nexuslabdata.connection.base.query import QueryExecResult, QueryWrapper
from nexuslabdata.exceptions import NotImplementedMethodException
from nexuslabdata.utils.mixin import NldMixIn


class DbService(NldMixIn, Generic[CONNECTION]):
    def __init__(
        self,
        connection_wrapper: CONNECTION,
    ) -> None:
        super().__init__()
        self.connection_wrapper = connection_wrapper

    def connection_is_opened(self) -> bool:
        if self.connection_wrapper is None:
            return False
        return self.connection_wrapper.is_opened()

    def open_connection(self) -> bool:
        if self.connection_wrapper is None:
            return False
        if self.connection_wrapper.is_opened():
            return True
        self.connection_wrapper.open()
        return self.connection_wrapper.is_opened()

    def close_connection(self) -> bool:
        if self.connection_wrapper is None:
            return False
        if self.connection_wrapper.is_closed():
            return True
        self.connection_wrapper.close()
        return self.connection_wrapper.is_closed()


DB_SERVICE = TypeVar("DB_SERVICE", bound=DbService[Any])


class SqlDbService(DbService[CONNECTION]):
    def __init__(self, connection_wrapper: CONNECTION) -> None:
        super().__init__(connection_wrapper)

    def log_execution_error(self, **kwargs: Any) -> None:
        """Logs an execution error"""
        raise NotImplementedMethodException(
            self.__class__, "log_execution_error"
        )

    def execute_query(self, query: Union[str, QueryWrapper]) -> QueryExecResult:
        """Executes a query"""
        raise NotImplementedMethodException(self.__class__, "execute_query")


SQL_DB_SERVICE = TypeVar("SQL_DB_SERVICE", bound=SqlDbService[Any])
