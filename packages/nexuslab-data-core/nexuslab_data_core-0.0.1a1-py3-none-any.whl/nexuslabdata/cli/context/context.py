from typing import Any, Dict, List, Optional, Union, cast

import click

import nexuslabdata.cli.cli_variables as cli_variables
from nexuslabdata.connection.base import ConnectionInfos
from nexuslabdata.connection.manager.factory import (
    ConnectionAdapterManagerFactory,
)
from nexuslabdata.connection.manager.manager import ConnectionServiceManager
from nexuslabdata.core.flow.execution.data_flow_execution import (
    DataFlowExecutionRunParam,
)
from nexuslabdata.project import Project
from nexuslabdata.task import ExecutionInfo
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn
from nexuslabdata.utils.import_utils import import_class_inside_module
from nexuslabdata.utils.mixin import NldMixIn


class ClickException(RuntimeError):
    pass


class NldCliDict(Dict[str, Any], NldMixIn):
    @property
    def exec_info(self) -> ExecutionInfo:
        assert cli_variables.EXC_INFO in list(self.keys())
        return cast(ExecutionInfo, self[cli_variables.EXC_INFO])

    @property
    def exec_uuid(self) -> str:
        return self.exec_info.uuid

    @property
    def params(self) -> Dict[str, Any]:
        assert cli_variables.PARAMS in list(self.keys())
        return cast(Dict[str, Any], self[cli_variables.PARAMS])

    @property
    def project_root_folder_path(self) -> str:
        assert cli_variables.PROJECT_ROOT_FOLDER_PATH in list(self.keys())
        return cast(str, self[cli_variables.PROJECT_ROOT_FOLDER_PATH])

    @property
    def profile_root_folder_path(self) -> str:
        assert cli_variables.PROFILE_ROOT_FOLDER_PATH in list(self.keys())
        return cast(str, self[cli_variables.PROFILE_ROOT_FOLDER_PATH])

    @property
    def project(self) -> Project:
        assert cli_variables.PROJECT in list(self.keys())
        return cast(Project, self[cli_variables.PROJECT])

    @property
    def connection_infos(
        self,
    ) -> ConnectionInfos:
        assert cli_variables.CONNECTION_INFOS in list(self.keys())
        return cast(ConnectionInfos, self[cli_variables.CONNECTION_INFOS])

    @property
    def connection_adapter_manager_factory(
        self,
    ) -> ConnectionAdapterManagerFactory:
        assert cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY in list(
            self.keys()
        )
        return cast(
            ConnectionAdapterManagerFactory,
            self[cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY],
        )

    @property
    def connection_service_manager(self) -> ConnectionServiceManager:
        return self.connection_adapter_manager_factory.conn_service_manager

    def get_task_context(self) -> Dict[str, Any]:
        task_context: Dict[str, Any] = {}
        if cli_variables.PROJECT in list(self.keys()):
            task_context.update({cli_variables.PROJECT: self.project})
        if cli_variables.PARAMS in list(self.keys()):
            task_context.update({cli_variables.PARAMS: self.params})
        task_context.update({cli_variables.EXC_INFO: self.exec_info})
        if cli_variables.CONNECTION_INFOS in list(self.keys()):
            task_context.update(
                {cli_variables.CONNECTION_INFOS: self.connection_infos}
            )
        if cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY in list(
            self.keys()
        ):
            task_context.update(
                {
                    cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY: self.connection_adapter_manager_factory
                }
            )
        return task_context

    def get_task_context_for_keys(
        self, keys: List[str], db_service_map: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Get the dictionary for task context, used for init of a task.

        DB Services can be retrieved using the db_service map which maps a db_service name
        with the correct connection profile, or simply with the name of the db service.

        :param keys: The list of expected keys
        :param db_service_map: The list of expected service keys mapped to the connection names
        :return: A dictionary to use for a task initialization
        """
        keys_without_db_service = [
            key for key in keys if not key.endswith("_db_service")
        ]
        keys_for_db_service = [
            key for key in keys if key.endswith("_db_service")
        ]
        db_service_map = {} if db_service_map is None else db_service_map

        task_context: Dict[str, Any] = {}
        known_keys = [
            cli_variables.CONTEXT_DICT,
            cli_variables.PROJECT,
            cli_variables.PARAMS,
            cli_variables.PROFILE_NAME,
            cli_variables.DATA_FLOW_NAME,
            cli_variables.EXC_INFO,
            cli_variables.CONNECTION_INFOS,
            cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY,
            cli_variables.CONNECTION_ADAPTER_MANAGER,
        ]
        db_service_names = []
        if cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY in list(
            self.keys()
        ):
            db_service_names = [
                service_name
                for service_name in self.connection_adapter_manager_factory.conn_service_manager.get_service_names()
            ]

        if any([key not in known_keys for key in keys_without_db_service]):
            raise click.ClickException(
                f"Task mandatory key is not available in the standard context. All requested keys are : {', '.join(keys)}"
            )
        for key in keys_without_db_service:
            if key == cli_variables.CONTEXT_DICT:
                task_context.update({key: self})
            elif key in list(self.keys()):
                task_context.update({key: self[key]})
            else:
                raise click.ClickException(
                    f"Key : {key} is not available in the task context but was requested for task execution"
                )

        if len(db_service_map) == 0:
            for key in keys_for_db_service:
                if key in list(self.keys()):
                    task_context.update({key: self[key]})
                else:
                    raise click.ClickException(
                        f"DB Service : {key} is not available in the task context but was requested for task execution"
                    )
        else:
            for key, connection_name in db_service_map.items():
                if connection_name in db_service_names:
                    task_context.update(
                        {
                            key
                            + "_db_service": self.connection_adapter_manager_factory.conn_service_manager.get_service(
                                connection_name
                            )
                        }
                    )
                else:
                    raise click.ClickException(
                        f"DB Service : {key} is not available in the task context but was requested for task execution"
                    )
        return task_context


class NldCliRunParams(Dict[str, Any]):
    @classmethod
    def from_data_flow_execution_run_params(
        cls,
        run_params: Union[
            DataFlowExecutionRunParam, List[DataFlowExecutionRunParam]
        ],
    ) -> "NldCliRunParams":
        new_obj = NldCliRunParams()
        run_params = (
            [run_params]
            if isinstance(run_params, DataFlowExecutionRunParam)
            else run_params
        )
        for run_param in run_params:
            if run_param.type is None:
                new_obj.update({run_param.name: run_param.content})
            else:
                module_name, class_type = import_class_inside_module(
                    run_param.type
                )
                if not issubclass(class_type, NldDataClassMixIn):
                    raise ValueError(
                        f"Run Parameter class {class_type} must inherit from NldDataClassMixIn"
                    )
                if isinstance(run_param.content, list):
                    run_param_content_list = run_param.content
                    current_param = []
                    for run_param_content in run_param_content_list:
                        current_param.append(class_type(**run_param_content))
                    new_obj.update({run_param.name: current_param})
                else:
                    new_obj.update(
                        {run_param.name: class_type(**run_param.content)}
                    )

        return new_obj


class NldCliContext(click.Context):
    def __init__(self, command: click.Command, **kwargs: Any) -> None:
        super().__init__(command=command, **kwargs)
        self.obj = NldCliDict()
        self.run_params = NldCliRunParams()
