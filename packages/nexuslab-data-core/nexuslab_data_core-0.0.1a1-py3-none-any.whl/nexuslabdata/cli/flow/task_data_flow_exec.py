from typing import Any, Type

from nexuslabdata.cli import cli_variables
from nexuslabdata.cli.cli_utils import execute_task_with_explicit_context
from nexuslabdata.cli.context import NldCliDict, NldCliRunParams
from nexuslabdata.connection.base.connection_info import ConnectionInfos
from nexuslabdata.connection.manager.factory import (
    ConnectionAdapterManagerFactory,
)
from nexuslabdata.core.flow import DataFlowExecution
from nexuslabdata.project import Project
from nexuslabdata.task import ExecutionInfo, StandardTask
from nexuslabdata.utils.import_utils import import_class_inside_module


class DataFlowExecTask(StandardTask):
    init_params = [
        cli_variables.CONTEXT_DICT,
        cli_variables.PROJECT,
        cli_variables.PROFILE_NAME,
        cli_variables.DATA_FLOW_NAME,
        cli_variables.EXC_INFO,
        cli_variables.CONNECTION_INFOS,
        cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY,
    ]
    run_params = []

    def __init__(
        self,
        context_dict: NldCliDict,
        project: Project,
        profile_name: str,
        data_flow_name: str,
        exc_info: ExecutionInfo,
        connection_infos: ConnectionInfos,
        connection_adapter_manager_factory: ConnectionAdapterManagerFactory,
    ):
        super().__init__(exc_info=exc_info, connection_infos=connection_infos)
        self.context_dict = context_dict
        self.project = project
        self.profile_name = profile_name
        self.data_flow_execution = (
            self.project.obj_service.get_data_flow_execution(data_flow_name)
        )
        self.exec_info = exc_info
        self.connection_infos = connection_infos

        # Initialize ConnectionServiceManager and factory
        self.factory = connection_adapter_manager_factory
        self.connection_manager = (
            connection_adapter_manager_factory.conn_service_manager
        )

        # Load task class from configuration
        self.task_class = self.load_task_class(self.data_flow_execution)

        # Verify db_services in the task configuration
        self._verify_db_services_available(self.data_flow_execution)

        # Initialize only required services
        self._initialize_services(profile_name)

    def _initialize_services(self, profile_name: str) -> None:
        self.connection_manager = self.factory.load_services(
            connection_infos=self.connection_infos,
            profile_name=profile_name,
            connection_names=self.data_flow_execution.get_db_service_connection_names(),
        )
        self.logger.info(
            f"Available services: {self.connection_manager.get_service_names()}"
        )
        for service_name in self.connection_manager.get_service_names():
            self.logger.info(f"Opening connection for service: {service_name}")
            try:
                self.connection_manager.open_service_connection(service_name)
                service = self.connection_manager.get_service(service_name)
                self.logger.info(
                    f"Connection initialized for {service_name}: {service.connection_wrapper.connection is not None}"
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to open connection for {service_name}: {str(e)}"
                )
                raise

    def load_task_class(
        self, data_flow_execution: DataFlowExecution
    ) -> Type[StandardTask]:
        task_class_path = data_flow_execution.task_class
        if not task_class_path:
            raise ValueError("No task_class specified in the data flow")

        try:
            module, task_class = import_class_inside_module(task_class_path)
            if not issubclass(task_class, StandardTask):
                raise ValueError(
                    f"Task class {task_class_path} must inherit from StandardTask"
                )
            return task_class
        except (ImportError, AttributeError, ValueError) as e:
            self.logger.error(
                f"Failed to load task class {task_class_path}: {str(e)}"
            )
            raise

    def _verify_db_services_available(
        self, data_flow_execution: DataFlowExecution
    ) -> None:
        """Verify that the db_services in the data flow are available in connection_infos."""
        if not data_flow_execution.db_services:
            self.logger.error("No db_services specified in the data flow")
            raise ValueError("No db_services specified in the data flow")

        required_service_connections = (
            data_flow_execution.get_db_service_connection_names()
        )
        available_service_connections = (
            self.connection_infos.get_connection_names()
        )
        # Ensure all required services are in db_services
        for required_service_connection in required_service_connections:
            if not any(
                available_service_connection == required_service_connection
                for available_service_connection in available_service_connections
            ):
                raise ValueError(
                    f"Required service {required_service_connection} not found in db_services"
                )
        self.logger.debug("All required db_services are available")

    def run(self, **run_params: Any) -> Any:
        """Execute the data flow task with the provided parameters."""
        try:
            self.logger.info(
                f"Starting data flow execution for data_flow_name: {self.data_flow_execution.name}, profile_name: {self.profile_name}"
            )
            return execute_task_with_explicit_context(
                self.task_class,
                context_dict=self.context_dict,
                run_params=NldCliRunParams.from_data_flow_execution_run_params(
                    self.data_flow_execution.run_params
                ),
                db_service_map=self.data_flow_execution.db_services,
            )

        except Exception as e:
            self.logger.error(f"Error during execution: {str(e)}")
            raise
        finally:
            # Close all services managed by ConnectionServiceManager
            self.connection_manager.close_all_service_connections()

    def interpret_results(self, results: Any) -> bool:
        """Interpret the results of the task execution."""
        return bool(results)
