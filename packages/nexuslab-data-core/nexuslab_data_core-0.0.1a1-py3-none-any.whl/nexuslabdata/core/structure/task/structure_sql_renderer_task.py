from typing import Any, Dict

from nexuslabdata.cli import cli_variables
from nexuslabdata.core.structure import SQLRendererWrapper
from nexuslabdata.core.structure.sql_renderer_wrapper import SQLRenderEntry
from nexuslabdata.project import Project
from nexuslabdata.service import NldServiceWrapper
from nexuslabdata.task.base_task import BaseRunStatus
from nexuslabdata.task.execution import ExecutionInfo
from nexuslabdata.task.std_task import StandardTask


class StructureSqlRendererTask(StandardTask):
    init_params = [
        cli_variables.PROJECT,
        cli_variables.EXC_INFO,
    ]
    run_params = []

    def __init__(
        self, project: Project, exc_info: ExecutionInfo, **kwargs: Any
    ) -> None:
        super().__init__(exc_info=exc_info, **kwargs)
        self.project = project
        self.exc_info = exc_info

    def _parse_params(self, raw: str) -> Dict[str, str]:
        """Parses the params passed via CLI into a dictionary."""
        params: Dict[str, str] = {}
        if raw:
            cleaned = raw.strip().lstrip("{").rstrip("}")
            param_pairs = [p.strip() for p in cleaned.split(",") if p.strip()]
            for pair in param_pairs:
                if "=" not in pair:
                    raise ValueError(f"Invalid param pair: '{pair}'")
                k, v = pair.split("=", 1)
                params[k.strip()] = v.strip()
        return params

    def run(  # type: ignore[override]
        self,
        structure: str,
        renderer: str,
        output_folder_name: str,
        *args: str,
        **kwargs: str,
    ) -> bool:
        run_status = BaseRunStatus.SUCCESS.value
        self.log_info("SQL rendering executing")

        # load params
        params = self._parse_params(kwargs["params"])

        # load structure object
        nld_service_wrapper: NldServiceWrapper = self.project.obj_service
        current_structure = nld_service_wrapper.get_structure(structure)
        if current_structure is None:
            raise ValueError(f"Structure not found: {structure}")

        # load renderer wrapper
        renderer_wrapper = nld_service_wrapper.get_sql_renderer(renderer)

        if renderer_wrapper is None and renderer.endswith(".sql"):
            renderer_wrapper = SQLRendererWrapper(
                name=structure,
                renderer=[SQLRenderEntry(name=renderer)],
            )
        if not renderer_wrapper:
            raise ValueError(f"Renderer not found: {renderer}")

        templates_dict = nld_service_wrapper.get_sql_template_dict()
        adapters_dict = nld_service_wrapper.get_structure_adapter_dict()

        try:
            renderer_wrapper.render_all(
                structure=current_structure,
                params=params,
                output_folder=output_folder_name,
                templates_dict=templates_dict,
                adapters_dict=adapters_dict,
            )
        except Exception as e:
            self.log_error(f"Structure rendering failed: {e}")
            raise

        self.log_info("SQL rendering done")
        return run_status
