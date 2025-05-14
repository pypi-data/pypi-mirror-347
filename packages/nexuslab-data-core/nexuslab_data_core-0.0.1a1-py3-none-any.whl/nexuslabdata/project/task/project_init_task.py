import os
from typing import Any

import nexuslabdata.project.default_project as default_project
from nexuslabdata.project import NLD_PROJECT_FILENAME, Project
from nexuslabdata.project.project_events import (
    ProjectAlreadyInitializedFolder,
    ProjectInitializationConfigError,
    ProjectInitializedSuccessfully,
)
from nexuslabdata.service import CONFIG_OBJECTS, MODEL_OBJECTS
from nexuslabdata.task import BaseRunStatus, StandardTask
from nexuslabdata.utils.file_util import create_empty_file

GITKEEP_FILE_NAME = ".gitkeep"


class ProjectInitTask(StandardTask):
    """
    Initializes a nld project in the folder where command line is launched
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # Project Root Path defaulted to the current directory
        self.project_root_path: str = os.path.join(os.getcwd(), "nld")

    def run(self, **kwargs: Any) -> bool:
        run_status = BaseRunStatus.SUCCESS.value

        # Check that the folder is not already initialized
        if not self._check_folder_initialized():
            self.log_event(
                ProjectAlreadyInitializedFolder(path=self.project_root_path)
            )
            return BaseRunStatus.FAIL.value

        # Initializes the folder for a project
        self._init_folder()

        self.log_event(
            ProjectInitializedSuccessfully(path=self.project_root_path)
        )

        return run_status

    def __get_project_folder_name(self) -> str:
        return os.path.basename(self.project_root_path)

    def __get_project_config_file_path(self) -> str:
        return os.path.join(self.project_root_path, NLD_PROJECT_FILENAME)

    def __get_default_project(self) -> Project:
        return default_project.get_default(self.project_root_path)

    def _check_folder_initialized(self) -> bool:
        # Check that the project configuration file does not exist
        project_config_file_path = self.__get_project_config_file_path()
        if os.path.exists(project_config_file_path):
            self.log_event(
                ProjectInitializationConfigError(path=project_config_file_path)
            )
            return BaseRunStatus.FAIL.value

        return BaseRunStatus.SUCCESS.value

    def _init_folder(self) -> bool:
        # Create the root folder if it does not exist
        os.makedirs(self.project_root_path, exist_ok=True)

        # Create the project configuration file
        with open(self.__get_project_config_file_path(), "w") as file:
            file.write(
                default_project.DEFAULT_PROJECT_YAML_FILE_CONTENT.replace(
                    "name: 'dummy' # Project Name to be changed",
                    f"name: '{self.__get_project_folder_name()}'",
                )
            )

        # Create all the project internal folders
        for cur_folder in self.__get_default_project().get_project_folders():
            os.makedirs(cur_folder, exist_ok=False)
            if os.path.basename(cur_folder) in ["data_flow", "structure"]:
                create_empty_file(os.path.join(cur_folder, GITKEEP_FILE_NAME))

        # Initialize all the config folders
        config_complete_path = os.path.join(
            self.__get_default_project().root_folder_path,
            self.__get_default_project().config_path,
        )
        for config_object in CONFIG_OBJECTS:
            config_object_path = os.path.join(
                config_complete_path, config_object.folder_name
            )
            os.makedirs(config_object_path, exist_ok=False)
            create_empty_file(
                os.path.join(config_object_path, GITKEEP_FILE_NAME)
            )

        # Initialize all the model folders
        model_complete_path = os.path.join(
            self.__get_default_project().root_folder_path,
            self.__get_default_project().model_path,
        )
        for model_object_definition in MODEL_OBJECTS:
            model_object_path = os.path.join(
                model_complete_path, model_object_definition.folder_name
            )
            os.makedirs(model_object_path, exist_ok=False)
            create_empty_file(
                os.path.join(model_object_path, GITKEEP_FILE_NAME)
            )

        return BaseRunStatus.SUCCESS.value
