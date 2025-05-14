from typing import Any

from nexuslabdata.cli import cli_variables
from nexuslabdata.core.structure.structure_builder import StructureBuilder
from nexuslabdata.project import Project
from nexuslabdata.service.nld_service_wrapper import NldServiceWrapper
from nexuslabdata.task.base_task import BaseRunStatus
from nexuslabdata.task.execution import ExecutionInfo
from nexuslabdata.task.std_task import StandardTask


class StructureBuildTask(StandardTask):
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

    def run(self, *args: str, **kwargs: str) -> bool:
        run_status = BaseRunStatus.SUCCESS.value
        self.log_info("Build structure executing")

        nld_service_wrapper: NldServiceWrapper = self.project.obj_service

        structure = nld_service_wrapper.get_structure(kwargs["structure"])
        structure_adapter = nld_service_wrapper.get_structure_adapter(
            kwargs["adapter"]
        )

        try:
            builder = StructureBuilder(
                name=kwargs["structure"],
                structure=structure,
                structure_adapter=structure_adapter,
                output_folder_name=kwargs["output_folder_name"],
            )
            builder.structure_builder()

        except Exception as e:
            self.log_error(f"Structure building failed: {e}")
            raise

        return run_status
