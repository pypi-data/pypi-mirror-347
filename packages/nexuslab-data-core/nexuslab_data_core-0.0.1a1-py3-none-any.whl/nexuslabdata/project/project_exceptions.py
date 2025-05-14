from typing import List

from nexuslabdata.exceptions import NldRuntimeException

####################################################################
##                     Project exceptions                         ##
####################################################################


class NldConfigError(NldRuntimeException):
    CODE = 1001
    MESSAGE = "NLD Configuration Error"


class NldProjectError(NldConfigError):
    CODE = 1101
    MESSAGE = "NLD Project Error"


class NldMissingProjectYamlFile(NldProjectError):
    CODE = 1102
    MESSAGE = "NLD Missing Project YAML File"

    def __init__(self, path: str) -> None:
        self.message = f"No nld_project.yml found at expected path {path}"


class NldProjectYamlMissingMandatoryKeys(NldProjectError):
    CODE = 1103
    MESSAGE = "NLD Project YAML File Missing Mandatory Keys"

    def __init__(self, missing_keys: List[str]) -> None:
        self.message = f"The project yaml is missing the mandatory keys : {', '.join(missing_keys)}"


class NldMissingProjectFolder(NldProjectError):
    CODE = 1110
    MESSAGE = "NLD Missing Project Folder"

    def __init__(self, folder_name: str, path: str) -> None:
        self.message = f"No {folder_name} found at expected path {path}"
