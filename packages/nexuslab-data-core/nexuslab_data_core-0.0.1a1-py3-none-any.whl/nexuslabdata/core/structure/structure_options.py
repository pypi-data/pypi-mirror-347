from dataclasses import dataclass
from enum import StrEnum, auto

from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class StructureOptionDefinition(NldNamedDataClassMixIn):
    name: str
    description: str


class StructureOptionNames(StrEnum):
    FILE_FORMAT = auto()


class StructureOptionDefinitions:
    """Generic constraints"""

    FILE_FORMAT = StructureOptionDefinition(
        name=StructureOptionNames.FILE_FORMAT.name,
        description="The file format",
    )
