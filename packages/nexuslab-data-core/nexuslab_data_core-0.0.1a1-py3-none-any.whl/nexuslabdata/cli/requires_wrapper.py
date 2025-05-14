from typing import Any, Callable

import click

from nexuslabdata.cli import requires
from nexuslabdata.utils import decorator_utils


def nld_command_wo_project_scope(command_name: str) -> Callable[[Any], Any]:
    return decorator_utils.composed(
        click.command(command_name),
        click.pass_context,
        requires.pre_processing,
        requires.manage_cli_exception,
    )


def nld_command(command_name: str) -> Callable[[Any], Any]:
    return decorator_utils.composed(
        click.command(command_name),
        click.pass_context,
        requires.pre_processing,
        requires.manage_cli_exception,
        requires.load_project,
    )
