from typing import Any, Tuple

from nexuslabdata.cli import requires_wrapper
from nexuslabdata.cli.cli_utils import execute_task
from nexuslabdata.project.task import ProjectInfoTask, ProjectInitTask


@requires_wrapper.nld_command_wo_project_scope("init")
def init(ctx: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return execute_task(ProjectInitTask, ctx)


@requires_wrapper.nld_command_wo_project_scope("info")
def info(ctx: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return execute_task(ProjectInfoTask, ctx)
