from typing import Any, Tuple

import click

from nexuslabdata.cli import cli_variables, params, requires
from nexuslabdata.cli.cli_utils import execute_task
from nexuslabdata.cli.flow.task_data_flow_exec import DataFlowExecTask


@click.command("execute")
@click.pass_context
@requires.pre_processing
@requires.manage_cli_exception
@requires.load_project
@requires.load_profiles
@params.data_flow_name
@params.profile_name
def flow_execute(
    ctx: click.Context, data_flow_name: str, profile_name: str, **kwargs: Any
) -> Tuple[Any, bool]:
    ctx.obj.update(
        {
            cli_variables.CONTEXT_DICT: ctx.obj,
            cli_variables.PROFILE_NAME: profile_name,
            cli_variables.DATA_FLOW_NAME: data_flow_name,
        }
    )
    return execute_task(DataFlowExecTask, ctx)
