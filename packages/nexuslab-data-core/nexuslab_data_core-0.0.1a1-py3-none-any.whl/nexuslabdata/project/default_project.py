import os

from nexuslabdata.project.project import Project

DEFAULT_PROJECT_YAML_FILE_CONTENT = """# Project Configuration
name: 'dummy' # Project Name to be changed
version: '0.0.1'

# Config configuration
config-path: 'config'

# Model configuration
model-path: 'model'

# Structure configuration
structure-path : 'structure'

# Data Flow configuration
data-flow-path : 'data_flow'"""


def get_default(root_folder_path: str) -> Project:
    return Project(
        root_folder_path=root_folder_path,
        name=os.path.basename(root_folder_path),
        version="0.0.1",
        config_path="config",
        model_path="model",
        structure_path="structure",
        data_flow_path="data_flow",
    )
