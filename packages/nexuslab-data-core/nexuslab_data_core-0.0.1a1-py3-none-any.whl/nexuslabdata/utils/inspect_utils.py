from inspect import getmembers
from types import ModuleType
from typing import Any


def extract_functions_from_command_module(
    command_module: ModuleType, command_prefix: str, command_type: type
) -> list[Any]:
    return [
        command[1]
        for command in getmembers(command_module)
        if command[0].startswith(command_prefix)
        and type(command[1]) is command_type
    ]
