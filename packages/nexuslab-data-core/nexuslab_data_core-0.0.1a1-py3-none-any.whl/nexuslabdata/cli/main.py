from typing import Any

import click

from nexuslabdata.cli.cli_utils import add_commands_from_modules
from nexuslabdata.cli.connection import main_connection
from nexuslabdata.cli.flow import main_flow
from nexuslabdata.cli.project import main_project
from nexuslabdata.cli.structure import main_structure


@click.group(no_args_is_help=True)  # type: ignore
@click.pass_context
def cli(ctx: Any, **kwargs: Any) -> Any | None:
    """Main command line for nld"""


@cli.group(no_args_is_help=True)  # type: ignore
@click.pass_context
def project(ctx: Any, **kwargs: Any) -> Any | None:
    """Main command line for project"""


add_commands_from_modules(project, main_project)


@cli.group(no_args_is_help=True)  # type: ignore
@click.pass_context
def connection(ctx: Any, **kwargs: Any) -> Any | None:
    """Main command line for connection"""


add_commands_from_modules(connection, main_connection)


@cli.group(no_args_is_help=True)  # type: ignore
@click.pass_context
def flow(ctx: Any, **kwargs: Any) -> Any | None:
    """Main command line for connection"""


add_commands_from_modules(flow, main_flow)


@cli.group(no_args_is_help=True)  # type: ignore
@click.pass_context
def structure(ctx: Any, **kwargs: Any) -> Any | None:
    """Main command line for structure"""


add_commands_from_modules(structure, main_structure)


if __name__ == "__main__":
    cli()
