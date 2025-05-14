from typing import Any, List

from nexuslabdata.cli import cli_variables
from nexuslabdata.connection.base import ConnectionInfos
from nexuslabdata.connection.manager.factory import (
    ConnectionAdapterManagerFactory,
)
from nexuslabdata.task import BaseRunStatus, StandardTask


class ConnectionDebugTask(StandardTask):
    """
    Debug a connection placed in a nld project
    """

    init_params: List[str] = [
        *StandardTask.init_params,
        cli_variables.CONNECTION_INFOS,
        cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY,
    ]
    run_params: List[str] = [*StandardTask.run_params, "connection_name"]

    def __init__(
        self,
        connection_infos: ConnectionInfos,
        connection_adapter_manager_factory: ConnectionAdapterManagerFactory,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.connection_infos = connection_infos
        self.connection_adapter_manager_factory = (
            connection_adapter_manager_factory
        )

    def run(self, connection_name: str, **kwargs: Any) -> bool:  # type: ignore[override]
        run_status = BaseRunStatus.SUCCESS.value

        profile_name = (
            kwargs["profile_name"]
            if "profile_name" in list(kwargs.keys())
            else None
        )

        try:
            connection_info = self.connection_infos.get_connection_info(
                connection_name
            )
            db_service = (
                self.connection_adapter_manager_factory.create_new_service(
                    connection_info, profile_name
                )
            )
            db_service.open_connection()
            self.log_info(
                f"DB Service opened successfully for connection name {connection_name}"
            )
        except Exception as e:
            if hasattr(e, "message"):
                self.log_error(
                    f"DB Service could not be opened due to the error : {e.__class__.__name__} with message '{e.message}'"
                )
            else:
                self.log_error(
                    f"DB Service could not be opened due to the error : {e.__class__.__name__} with message '{e}'"
                )

        return run_status
