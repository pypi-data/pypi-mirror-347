from typing import Type

from nexuslabdata.exceptions import NldRuntimeException
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


class ObjectReadNoDirectoryException(NldRuntimeException):
    CODE = 21101
    MESSAGE = "No directory found during the read of object"

    def __init__(
        self, folder_path: str, data_class: Type[NldDataClassMixIn]
    ) -> None:
        self.message = (
            f"Load from folder {folder_path} for object {data_class.get_data_class_schema().schema_name} "
            f"failed due to non-existant folder."
        )
