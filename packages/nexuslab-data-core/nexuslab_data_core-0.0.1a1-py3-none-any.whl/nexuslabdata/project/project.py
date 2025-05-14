import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from nexuslabdata.project.project_exceptions import (
    NldMissingProjectYamlFile,
    NldProjectError,
    NldProjectYamlMissingMandatoryKeys,
)
from nexuslabdata.service.config_service import ConfigService
from nexuslabdata.service.data_flow_service import DataFlowService
from nexuslabdata.service.model_service import ModelService
from nexuslabdata.service.nld_service_wrapper import (
    NldServiceWrapper,
    create_nld_service_wrapper,
)
from nexuslabdata.service.structure_service import StructureService
from nexuslabdata.utils.yaml_util import load_yaml_file_into_dict

NLD_PROJECT_FILENAME = "nld_project.yml"


def load_project_to_dict(root_path: str) -> Dict[str, Any]:
    root_path = os.path.normpath(root_path)
    project_filepath = os.path.join(root_path, NLD_PROJECT_FILENAME)

    if not os.path.exists(project_filepath):
        raise NldMissingProjectYamlFile(path=project_filepath)

    project_dict = load_yaml_file_into_dict(project_filepath)

    if not isinstance(project_dict, dict):
        raise NldProjectError(
            f"{NLD_PROJECT_FILENAME} does not parse to a dictionary"
        )

    return project_dict


@dataclass
class Project:
    root_folder_path: str
    name: str
    version: Optional[str]
    config_path: str
    model_path: str
    structure_path: str
    data_flow_path: str
    obj_service: NldServiceWrapper = NldServiceWrapper(
        ConfigService(), ModelService(), StructureService(), DataFlowService()
    )

    @classmethod
    def from_yaml(
        cls, root_path: str, load_obj_service: bool = True
    ) -> "Project":
        from_dict = load_project_to_dict(root_path)

        project_key_list = [
            "name",
            "version",
            "config-path",
            "model-path",
            "structure-path",
            "data-flow-path",
        ]
        missing_keys_in_dict = [
            project_key
            for project_key in project_key_list
            if project_key not in list(from_dict.keys())
        ]
        if len(missing_keys_in_dict) > 0:
            raise NldProjectYamlMissingMandatoryKeys(
                missing_keys=missing_keys_in_dict
            )

        # Project Configuration
        root_folder_path = root_path
        name = from_dict["name"]
        version = from_dict["version"]
        config_path = from_dict["config-path"]
        model_path = from_dict["model-path"]
        structure_path = from_dict["structure-path"]
        data_flow_path = from_dict["data-flow-path"]
        obj_service = create_nld_service_wrapper(
            root_folder_path,
            config_folder_name=config_path,
            model_folder_name=model_path,
            structure_folder_name=structure_path,
            data_flow_folder_name=data_flow_path,
            load_obj_service=load_obj_service,
        )

        project = Project(
            root_folder_path=root_folder_path,
            name=name,
            version=version,
            config_path=config_path,
            model_path=model_path,
            structure_path=structure_path,
            data_flow_path=data_flow_path,
            obj_service=obj_service,
        )

        return project

    def get_project_folders(self) -> List[str]:
        project_folders: List[str] = list()
        project_folders.append(
            os.path.join(self.root_folder_path, self.config_path)
        )
        project_folders.append(
            os.path.join(self.root_folder_path, self.model_path)
        )
        project_folders.append(
            os.path.join(self.root_folder_path, self.structure_path)
        )
        project_folders.append(
            os.path.join(self.root_folder_path, self.data_flow_path)
        )
        return project_folders

    def get_template_content(self, template_name: str) -> str:
        template_path = os.path.join(
            self.model_path, "sql_template", f"{template_name}.jinja2"
        )
        if not os.path.isfile(template_path):
            raise FileNotFoundError(
                f"Template Jinja not found: {template_path}"
            )

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
