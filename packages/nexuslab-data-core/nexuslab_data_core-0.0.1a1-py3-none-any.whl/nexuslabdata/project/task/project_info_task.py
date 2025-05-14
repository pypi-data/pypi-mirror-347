import os
from typing import Any

from nexuslabdata.project.project import Project
from nexuslabdata.service import DATA_FLOW_OBJECTS, MODEL_OBJECTS
from nexuslabdata.task import BaseRunStatus, StandardTask


class ProjectInfoTask(StandardTask):
    """
    Provides information about the project
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # Project Root Path defaulted to the current directory
        self.project_root_path: str = os.path.join(os.getcwd())

    def run(self, **kwargs: Any) -> bool:
        run_status = BaseRunStatus.SUCCESS.value

        project = Project.from_yaml(self.project_root_path)
        self.log_info(f"Current Project name is : {project.name}")
        self.log_info(f"")

        self.log_info(f"Model Objects ----------------------------")
        for model_object_definition in MODEL_OBJECTS:
            self.log_info(
                f"{model_object_definition.get_data_class_name()} : "
                f"{len(project.obj_service.model_service.get_object_keys(model_object_definition.name))}"
            )
        self.log_info(f"")

        self.log_info(f"Structure Objects ------------------------")
        self.log_info(
            f"Structures : " f"{len(project.obj_service.get_structure_keys())}"
        )
        self.log_info(f"")

        self.log_info(f"Data Flow Objects ------------------------")
        for data_flow_object_definition in DATA_FLOW_OBJECTS:
            self.log_info(
                f"{data_flow_object_definition.get_data_class_name()} : "
                f"{len(project.obj_service.data_flow_service.get_object_keys(data_flow_object_definition.name))}"
            )
        self.log_info(f"")

        return run_status
