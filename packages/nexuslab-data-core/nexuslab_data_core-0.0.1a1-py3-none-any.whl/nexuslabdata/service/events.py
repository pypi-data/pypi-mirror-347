from typing import Type

from nexuslabdata.logging import DebugEvent
from nexuslabdata.utils.data_class_mixin import DATA_CLASS_MIX_IN


class DataClassReadFromDirectoryStartEvent(DebugEvent):
    def __init__(
        self,
        data_class: Type[DATA_CLASS_MIX_IN],
        root_path: str,
    ) -> None:
        self.data_class = data_class
        self.root_path = root_path

    def code(self) -> str:
        return "M-101"

    def message(self) -> str:
        return f"{self.data_class.get_data_class_schema().schema_name} load started on folder : {self.root_path}"


class DataClassReadFromDirectoryCompletedSuccessfullyEvent(DebugEvent):
    def __init__(
        self,
        data_class: Type[DATA_CLASS_MIX_IN],
    ) -> None:
        self.data_class = data_class

    def code(self) -> str:
        return "M-102"

    def message(self) -> str:
        return f"{self.data_class.get_data_class_schema().schema_name} load completed"
