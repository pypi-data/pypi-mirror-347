from typing import Any, Dict, List

from nexuslabdata.connection.base import DbService
from nexuslabdata.connection.base.exceptions import (
    DbServiceAlreadyAvailableException,
    NoDbServiceAvailableException,
)
from nexuslabdata.utils.mixin import NldMixIn


class ConnectionServiceManager(NldMixIn):
    def __init__(self) -> None:
        super().__init__()
        self.services: Dict[str, DbService[Any]] = {}

    def add_service(
        self,
        name: str,
        db_service: DbService[Any],
    ) -> None:
        if name in list(self.services.keys()):
            raise DbServiceAlreadyAvailableException(name)
        self.services.update({name: db_service})

    def get_service_names(self) -> List[str]:
        return list(self.services.keys())

    def get_service(self, name: str) -> DbService[Any]:
        if name not in list(self.services.keys()):
            raise NoDbServiceAvailableException(name)
        return self.services[name]

    def open_service_connection(self, name: str) -> None:
        self.get_service(name).open_connection()

    def close_service_connection(self, name: str) -> bool:
        service = self.get_service(name)
        service.close_connection()
        return service.connection_wrapper.is_closed()  # type: ignore[no-any-return]

    def close_all_service_connections(self) -> bool:
        all_connections_closed = True
        for service_name in self.get_service_names():
            if not self.close_service_connection(service_name):
                all_connections_closed = False
        return all_connections_closed
