from typing import Any, Dict, Generic, Type

from nexuslabdata.connection.base.connection import CONNECTION
from nexuslabdata.connection.base.credential import CREDENTIAL_TYPE
from nexuslabdata.connection.base.service import DB_SERVICE


class ConnectionAdapterPlugin(Generic[DB_SERVICE, CONNECTION, CREDENTIAL_TYPE]):
    """Defines the basic requirements for a connection plugin"""

    def __init__(
        self,
        service_class: Type[DB_SERVICE],
        connection_wrapper_class: Type[CONNECTION],
        credentials_class: Type[CREDENTIAL_TYPE],
        include_path: str,
    ):
        self.service_class: Type[DB_SERVICE] = service_class
        self.connection_wrapper_class: Type[
            CONNECTION
        ] = connection_wrapper_class
        self.credentials_class: Type[CREDENTIAL_TYPE] = credentials_class
        self.include_path: str = include_path

    def create_new_credentials(
        self, credentials_dict: Dict[str, Any]
    ) -> CREDENTIAL_TYPE:
        return self.credentials_class(**credentials_dict)

    def create_new_connection_wrapper(
        self, name: str, credentials_dict: Dict[str, Any]
    ) -> CONNECTION:
        return self.connection_wrapper_class(
            name=name, credentials=self.create_new_credentials(credentials_dict)
        )

    def create_new_service(
        self, name: str, credentials_dict: Dict[str, Any]
    ) -> DB_SERVICE:
        return self.service_class(
            connection_wrapper=self.create_new_connection_wrapper(
                name, credentials_dict
            )
        )
