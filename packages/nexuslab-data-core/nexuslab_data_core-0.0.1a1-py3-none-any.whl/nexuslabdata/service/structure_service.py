from nexuslabdata.core import Structure
from nexuslabdata.service.object_std_service import (
    ObjectDefinition,
    ObjectStandardProviderService,
)
from nexuslabdata.utils import NldStrEnum


class StructureObjectNames(NldStrEnum):
    STRUCTURE = "structure"


class StructureObjects:
    STRUCTURE = ObjectDefinition(
        name=StructureObjectNames.STRUCTURE.value,
        data_class=Structure,
        folder_name=".",
    )


class StructureService(ObjectStandardProviderService):
    def __init__(self) -> None:
        object_definitions = [
            StructureObjects.STRUCTURE,
        ]
        super().__init__(object_definitions=object_definitions)
