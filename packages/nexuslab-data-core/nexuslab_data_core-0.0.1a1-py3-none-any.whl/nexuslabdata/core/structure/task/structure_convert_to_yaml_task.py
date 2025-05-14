import os
from typing import Any, Optional

from nexuslabdata.cli import cli_variables
from nexuslabdata.core import Structure, StructureCsvAdapter
from nexuslabdata.exceptions import (
    MissingObjectException,
    NoObjectLoadedException,
)
from nexuslabdata.project import Project
from nexuslabdata.service import StructureObjects
from nexuslabdata.task.base_task import BaseRunStatus
from nexuslabdata.task.execution import ExecutionInfo
from nexuslabdata.task.std_task import StandardTask
from nexuslabdata.utils.datetime_util import (
    get_current_datetime_as_filesystem_friendly_str,
)
from nexuslabdata.utils.yaml_util import dump_dict_to_yaml


class StructureConvertToYamlTask(StandardTask):
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

    def run(  # type: ignore[override]
        self,
        structure: str,
        output_folder_name: Optional[str],
        *args: str,
        **kwargs: str,
    ) -> bool:
        run_status = BaseRunStatus.SUCCESS.value
        self.log_info("Structure conversion to yaml - Started")

        structure_object_definition = StructureObjects.STRUCTURE
        structure_folder_path = os.path.join(
            self.project.root_folder_path,
            self.project.structure_path,
            structure_object_definition.folder_name,
        )
        structure_file_path = os.path.join(
            structure_folder_path, f"{structure}.csv"
        )

        if not os.path.exists(structure_file_path):
            raise MissingObjectException(Structure, structure)

        structure_list = StructureCsvAdapter().read_csv_from_file(
            structure_file_path
        )
        if len(structure_list) == 0:
            raise NoObjectLoadedException(Structure, structure_file_path)

        structure_read = structure_list[0]

        # Create output directory
        output_folder_name = (
            output_folder_name
            or get_current_datetime_as_filesystem_friendly_str()
        )

        output_dir = os.path.join("output", output_folder_name)
        os.makedirs(output_dir, exist_ok=True)

        yaml_path = os.path.join(output_dir, f"{structure_read.name}.yml")
        dump_dict_to_yaml(structure_read.to_dict(), yaml_path)

        self.log_info("Structure conversion to yaml - Successful")

        return run_status
