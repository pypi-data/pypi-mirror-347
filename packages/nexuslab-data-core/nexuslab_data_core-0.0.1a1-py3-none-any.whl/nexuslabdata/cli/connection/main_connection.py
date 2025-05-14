from typing import Any, Tuple

import click

from nexuslabdata.cli import params, requires
from nexuslabdata.cli.cli_utils import execute_task
from nexuslabdata.cli.connection import requires_connection
from nexuslabdata.connection.task import ConnectionDebugTask


@click.command("debug")
@click.pass_context
@requires.pre_processing
@requires.manage_cli_exception
@requires.load_profiles
@requires_connection.prepare_debug_run_params
@params.specific_connection_params
def debug(ctx: click.Context, **kwargs: Any) -> Tuple[bool, Any]:
    return execute_task(ConnectionDebugTask, ctx)
