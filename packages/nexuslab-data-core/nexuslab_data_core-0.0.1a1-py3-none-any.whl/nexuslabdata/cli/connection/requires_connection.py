from functools import update_wrapper
from typing import Any, Callable

import click

from nexuslabdata.cli.context import NldCliDict, NldCliRunParams


def prepare_debug_run_params(
    func: Any,
) -> Callable[[tuple[Any, ...], dict[str, Any]], Any]:
    """The decorator that handles the run parameters preparation"""

    def wrapper(*args, **kwargs):  # type: ignore
        ctx = args[0]
        assert isinstance(ctx, click.Context)
        assert isinstance(ctx.obj, NldCliDict)
        assert isinstance(ctx.run_params, NldCliRunParams)  # type: ignore[attr-defined]

        if "connection_name" in list(ctx.obj.params.keys()):
            ctx.run_params.update(  # type: ignore[attr-defined]
                {"connection_name": ctx.obj.params["connection_name"]}
            )
        if "profile_name" in list(ctx.obj.params.keys()):
            ctx.run_params.update(  # type: ignore[attr-defined]
                {"profile_name": ctx.obj.params["profile_name"]}
            )

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)
