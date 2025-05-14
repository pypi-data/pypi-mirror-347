import dataclasses
from typing import Any, Dict, List, Optional

from nexuslabdata.connection.base.exceptions import (
    UnavailableConnectionException,
    UnavailableConnectionProfileException,
)
from nexuslabdata.utils.data_class_mixin import (
    NldDataClassMixIn,
    NldNamedDataClassMixIn,
)


@dataclasses.dataclass
class ConnectionInfo(NldNamedDataClassMixIn):
    name: str
    type: str
    default_profile: str
    profiles: Dict[str, Dict[str, Any]]

    def get_profile_names(self) -> List[str]:
        return list(self.profiles.keys())

    def get_parameters_for_profile(
        self, profile_name: Optional[str] = None
    ) -> Dict[str, Any]:
        profile_name = (
            self.default_profile if profile_name is None else profile_name
        )
        if profile_name not in list(self.profiles.keys()):
            raise UnavailableConnectionProfileException(self.name, profile_name)
        return self.profiles[profile_name]


@dataclasses.dataclass
class ConnectionInfos(NldDataClassMixIn):
    connections: Dict[str, ConnectionInfo]

    def get_connection_names(self) -> List[str]:
        return list(self.connections.keys())

    def get_connection_info(self, connection_name: str) -> ConnectionInfo:
        if connection_name not in list(self.connections.keys()):
            raise UnavailableConnectionException(connection_name)
        return self.connections[connection_name]

    def get_connection_types(self) -> List[str]:
        return list(
            set(
                [
                    connection_info.type
                    for connection_info in self.connections.values()
                ]
            )
        )
