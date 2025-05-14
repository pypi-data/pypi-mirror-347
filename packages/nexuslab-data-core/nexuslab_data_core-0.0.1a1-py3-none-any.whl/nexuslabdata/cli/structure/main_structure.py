from typing import Any, Tuple

from nexuslabdata.cli import params, requires, requires_wrapper
from nexuslabdata.cli.cli_utils import execute_task
from nexuslabdata.core.structure.task.structure_build_task import (
    StructureBuildTask,
)
from nexuslabdata.core.structure.task.structure_convert_to_yaml_task import (
    StructureConvertToYamlTask,
)
from nexuslabdata.core.structure.task.structure_sql_renderer_task import (
    StructureSqlRendererTask,
)


@requires_wrapper.nld_command("render")
@requires.load_params_into_run_params
@params.specific_sql_renderer_params
def render(ctx: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return execute_task(StructureSqlRendererTask, ctx)


@requires_wrapper.nld_command("build")
@requires.load_params_into_run_params
@params.specific_structure_build_params
def build(ctx: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return execute_task(StructureBuildTask, ctx)


@requires_wrapper.nld_command("convert-to-yaml")
@requires.load_params_into_run_params
@params.specific_structure_convert_to_yaml_params
def convert_to_yaml(ctx: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return execute_task(StructureConvertToYamlTask, ctx)
