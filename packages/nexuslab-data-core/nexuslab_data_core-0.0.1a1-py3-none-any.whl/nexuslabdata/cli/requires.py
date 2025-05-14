import os
import uuid
from functools import update_wrapper
from typing import Any, Callable, Optional

from click import Context

from nexuslabdata.cli import cli_variables
from nexuslabdata.cli.cli_events import (
    CommandCompleted,
    CommandRuntimeError,
    CommandStarted,
    ConnectionFactoryLoadedSuccessfully,
    ProjectLoadedSuccessfully,
)
from nexuslabdata.cli.cli_exceptions import ExceptionExit
from nexuslabdata.cli.context import NldCliDict, NldCliRunParams
from nexuslabdata.connection.base import ConnectionInfos
from nexuslabdata.connection.manager.factory import (
    ConnectionAdapterManagerFactory,
)
from nexuslabdata.logging import EventLevel, LoggerManager, log_event_default
from nexuslabdata.project import Project
from nexuslabdata.task import ExecutionInfo
from nexuslabdata.utils import datetime_util


def _init_logger(event_level: Optional[EventLevel] = None) -> None:
    if event_level is not None:
        LoggerManager(level=event_level)
    else:
        LoggerManager(level=EventLevel.DEBUG)


def pre_processing(func: Any):  # type: ignore
    """The decorator that handles all the preprocessing tasks for the click commands.
    This decorator must be the first decorator to declare.
    It initializes the logger manager, the context object dictionary and the execution information
    """

    def wrapper(*args, **kwargs):  # type: ignore
        ctx = args[0]
        assert isinstance(ctx, Context)

        # Initializes the logger, execution information and log command start
        _init_logger()
        exec_info = ExecutionInfo(
            command=ctx.command_path,
            uuid=uuid.uuid4().__str__(),
            started_at=datetime_util.get_current_datetime(),
            success=None,
            completed_at=None,
        )
        ctx.obj = NldCliDict({cli_variables.EXC_INFO: exec_info})
        ctx.obj.update(
            {cli_variables.PARAMS: ctx.params if ctx.params is not None else {}}
        )

        ctx.run_params = NldCliRunParams()  # type: ignore[attr-defined]

        log_event_default(CommandStarted(exec_info=exec_info))

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def manage_cli_exception(func: Any):  # type: ignore
    """The decorator that handles all exception handling for the click commands.
    This decorator must be used before any other decorators that may throw an exception.
    """

    def wrapper(*args, **kwargs):  # type: ignore
        ctx = args[0]

        success = False

        try:
            result, success = func(*args, **kwargs)
        except (Exception, RuntimeError) as e:
            log_event_default(CommandRuntimeError(e=e))
            raise ExceptionExit(e)
        finally:
            exec_info: ExecutionInfo = ctx.obj[cli_variables.EXC_INFO]
            exec_info.success = success
            exec_info.completed_at = datetime_util.get_current_datetime()
            log_event_default(CommandCompleted(exec_info=exec_info))
        return result, success

    return update_wrapper(wrapper, func)


def load_project(func: Any):  # type: ignore
    """The decorator that handles the project load into memory"""

    def wrapper(*args, **kwargs):  # type: ignore
        ctx = args[0]
        assert isinstance(ctx, Context)
        assert isinstance(ctx.obj, NldCliDict)

        # Initializes the logger, execution information and log command start
        project_root_folder_path = os.getcwd()
        ctx.obj.update(
            {cli_variables.PROJECT_ROOT_FOLDER_PATH: project_root_folder_path}
        )

        project = Project.from_yaml(project_root_folder_path)
        ctx.obj.update({cli_variables.PROJECT: project})

        log_event_default(ProjectLoadedSuccessfully())

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def load_profiles(
    func: Any,
) -> Callable[[tuple[Any, ...], dict[str, Any]], Any]:
    """The decorator that handles the connection service factory load into memory

    Should be executed after load_project()"""

    def wrapper(*args, **kwargs):  # type: ignore
        ctx = args[0]
        assert isinstance(ctx, Context)
        assert isinstance(ctx.obj, NldCliDict)

        # Initializes the logger, execution information and log command start
        profile_root_folder_path = os.getcwd()
        ctx.obj.update(
            {cli_variables.PROFILE_ROOT_FOLDER_PATH: profile_root_folder_path}
        )

        with open(
            os.path.join(profile_root_folder_path, "profiles.yml"), "r"
        ) as file:
            connection_info_content = file.read()
        connection_infos = ConnectionInfos.from_yaml(connection_info_content)

        ctx.obj.update({cli_variables.CONNECTION_INFOS: connection_infos})

        factory = ConnectionAdapterManagerFactory()
        for connection_type in connection_infos.get_connection_types():
            factory.load_plugin(connection_type)

        ctx.obj.update(
            {cli_variables.CONNECTION_ADAPTER_MANAGER_FACTORY: factory}
        )

        log_event_default(ConnectionFactoryLoadedSuccessfully())

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def load_params_into_run_params(
    func: Any,
) -> Callable[[tuple[Any, ...], dict[str, Any]], Any]:
    """The decorator that loads the run params directly from the cli params"""

    def wrapper(*args, **kwargs):  # type: ignore
        ctx = args[0]
        assert isinstance(ctx, Context)
        assert isinstance(ctx.obj, NldCliDict)
        assert isinstance(ctx.run_params, NldCliRunParams)  # type: ignore[attr-defined]

        for key, value in ctx.obj.params.items():
            ctx.run_params.update({key: value})  # type: ignore[attr-defined]

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)
