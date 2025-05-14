import traceback
from importlib import import_module
from typing import Any, Dict, List, Optional, Type

from nexuslabdata.connection.base import ConnectionInfo, ConnectionInfos
from nexuslabdata.connection.base.credential import BaseConnectionCredential
from nexuslabdata.connection.base.plugin import ConnectionAdapterPlugin
from nexuslabdata.connection.base.service import DbService
from nexuslabdata.connection.manager.events import (
    ConnectionAdapterPluginImportError,
    ConnectionAdapterPluginLoadError,
    ConnectionAdapterPluginLoadSuccessful,
)
from nexuslabdata.connection.manager.manager import ConnectionServiceManager
from nexuslabdata.exceptions import NldRuntimeException
from nexuslabdata.utils.mixin import NldMixIn


class ConnectionAdapterManagerFactory(NldMixIn):
    def __init__(self) -> None:
        super().__init__()
        self.plugins: Dict[str, ConnectionAdapterPlugin[Any, Any, Any]] = {}
        self.conn_service_manager: ConnectionServiceManager = (
            ConnectionServiceManager()
        )

    def load_plugin(
        self, connection_type: str
    ) -> Type[BaseConnectionCredential]:
        try:
            # mypy doesn't think modules have any attributes.
            mod: Any = import_module(
                "." + connection_type, "nexuslabdata.connection"
            )
        except ModuleNotFoundError as exc:
            # if we failed to import the target module in particular, inform
            # the user about it via a runtime error
            if exc.name == "nexuslabdata.connection." + connection_type:
                self.log_event(ConnectionAdapterPluginImportError(exc=str(exc)))
                raise NldRuntimeException(
                    f"Could not find adapter type {connection_type}!"
                )
            # otherwise, the error had to have come from some underlying
            # library. Log the stack trace.
            self.log_event(
                ConnectionAdapterPluginLoadError(
                    exc_info=traceback.format_exc()
                )
            )
            raise

        plugin: ConnectionAdapterPlugin[Any, Any, Any] = mod.Plugin
        self.plugins[connection_type] = plugin
        self.log_event(
            ConnectionAdapterPluginLoadSuccessful(type=connection_type)
        )

        return plugin.credentials_class

    def get_plugin(
        self, connection_type: str
    ) -> ConnectionAdapterPlugin[Any, Any, Any]:
        if connection_type in list(self.plugins.keys()):
            return self.plugins[connection_type]
        connection_types = ", ".join(list(self.plugins.keys()))

        message = f"Invalid connection adapter type {connection_type}! Must be one of {connection_types}"
        raise NldRuntimeException(message)

    def load_services(
        self,
        connection_infos: ConnectionInfos,
        profile_name: Optional[str] = None,
        connection_names: Optional[List[str]] = None,
    ) -> ConnectionServiceManager:
        connection_names = (
            connection_infos.get_connection_names()
            if connection_names is None
            else connection_names
        )
        for connection_name in connection_names:
            self.conn_service_manager.add_service(
                connection_name,
                self.create_new_service(
                    connection_info=connection_infos.get_connection_info(
                        connection_name
                    ),
                    profile_name=profile_name,
                ),
            )
        return self.conn_service_manager

    def create_new_service(
        self,
        connection_info: ConnectionInfo,
        profile_name: Optional[str] = None,
    ) -> DbService[Any]:
        assert connection_info is not None
        plugin = self.get_plugin(connection_info.type)
        return plugin.create_new_service(  # type: ignore[no-any-return]
            name=connection_info.name,
            credentials_dict=connection_info.get_parameters_for_profile(
                profile_name
            ),
        )
