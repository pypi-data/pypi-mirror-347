from inspect import getmembers
from types import ModuleType
from typing import Any, Dict, Optional, Tuple, Type

import click
import click.core

from nexuslabdata.cli.context import NldCliDict, NldCliRunParams
from nexuslabdata.task import BaseTask


def extract_functions_from_command_module(
    command_module: ModuleType, command_prefix: str, command_type: type
) -> list[Any]:
    return [
        command[1]
        for command in getmembers(command_module)
        if command[0].startswith(command_prefix)
        and type(command[1]) is command_type
    ]


def add_commands_from_modules(
    cli: click.core.Group, command_module: ModuleType, command_prefix: str = ""
) -> None:
    for method in extract_functions_from_command_module(
        command_module, command_prefix, click.core.Command
    ):
        cli.add_command(method)


def execute_task(task: Type[BaseTask], ctx: click.Context) -> Tuple[Any, bool]:
    assert isinstance(ctx, click.Context)
    assert isinstance(ctx.obj, NldCliDict)  # type: ignore[attr-defined]
    assert isinstance(ctx.run_params, NldCliRunParams)  # type: ignore[attr-defined]
    init_params_dict = ctx.obj.get_task_context_for_keys(task.init_params)
    run_params_dict = ctx.run_params  # type: ignore[attr-defined]
    task.check_init_params_dict(init_params_dict)
    task.check_run_params_dict(run_params_dict)
    task_inst = task(**init_params_dict)
    results = task_inst.run(**run_params_dict)  # type: ignore[attr-defined]
    success = task_inst.interpret_results(results)
    return results, success


def execute_task_with_explicit_context(
    task: Type[BaseTask],
    context_dict: NldCliDict,
    run_params: NldCliRunParams,
    db_service_map: Optional[Dict[str, str]] = None,
) -> Tuple[Any, bool]:
    assert isinstance(context_dict, NldCliDict)
    assert isinstance(run_params, NldCliRunParams)
    init_params_dict = context_dict.get_task_context_for_keys(
        task.init_params, db_service_map=db_service_map
    )
    run_params_dict = run_params  # type: ignore[attr-defined]
    task.check_init_params_dict(init_params_dict)
    task.check_run_params_dict(run_params_dict)
    task_inst = task(**init_params_dict)
    results = task_inst.run(**run_params_dict)  # type: ignore[attr-defined]
    success = task_inst.interpret_results(results)
    return results, success
