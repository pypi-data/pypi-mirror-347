from dataclasses import dataclass
from typing import Dict, List, Optional

from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class StructureCharacterisationDefinition(NldNamedDataClassMixIn):
    name: str
    description: str
    allowed_attributes: Optional[List[str]]
    linked_to_fields: bool = True
    allowed_multiple_characterisations_per_structure: bool = False


class StructureCharacterisationDefinitionAttributesNames(NldStrEnum):
    ENFORCED = "ENFORCED"


class StructureCharacterisationDefinitionNames(NldStrEnum):
    PRIMARY_KEY = "PRIMARY_KEY"
    TECHNICAL_UNIQUE_KEY = "TECHNICAL_UNIQUE_KEY"
    FUNCTIONAL_UNIQUE_KEY = "FUNCTIONAL_UNIQUE_KEY"
    UNIQUE = "UNIQUE"


class StructureCharacterisationDefinitions:
    PRIMARY_KEY = StructureCharacterisationDefinition(
        name=StructureCharacterisationDefinitionNames.PRIMARY_KEY.value,
        description="Primary Key",
        allowed_attributes=[
            StructureCharacterisationDefinitionAttributesNames.ENFORCED
        ],
        linked_to_fields=True,
        allowed_multiple_characterisations_per_structure=False,
    )
    TECHNICAL_UNIQUE_KEY = StructureCharacterisationDefinition(
        name=StructureCharacterisationDefinitionNames.TECHNICAL_UNIQUE_KEY.value,
        description="Technical Unique Key, defines the uniqueness of records in the table based on the fields "
        "linked to this technical key",
        allowed_attributes=[],
        linked_to_fields=True,
        allowed_multiple_characterisations_per_structure=False,
    )
    FUNCTIONAL_UNIQUE_KEY = StructureCharacterisationDefinition(
        name=StructureCharacterisationDefinitionNames.FUNCTIONAL_UNIQUE_KEY.value,
        description="Functional Unique Key, defines the uniqueness of records in the table based on the fields "
        "linked to this functional key",
        allowed_attributes=[],
        linked_to_fields=True,
        allowed_multiple_characterisations_per_structure=False,
    )
    UNIQUE = StructureCharacterisationDefinition(
        name=StructureCharacterisationDefinitionNames.UNIQUE.value,
        description="Uniqueness of records of the list of fields",
        allowed_attributes=[],
        linked_to_fields=True,
        allowed_multiple_characterisations_per_structure=True,
    )


STRUCTURE_CHARACTERISATION_DEFINITIONS: Dict[
    str, StructureCharacterisationDefinition
] = {
    StructureCharacterisationDefinitions.PRIMARY_KEY.name: StructureCharacterisationDefinitions.PRIMARY_KEY,
    StructureCharacterisationDefinitions.TECHNICAL_UNIQUE_KEY.name: StructureCharacterisationDefinitions.TECHNICAL_UNIQUE_KEY,
    StructureCharacterisationDefinitions.FUNCTIONAL_UNIQUE_KEY.name: StructureCharacterisationDefinitions.FUNCTIONAL_UNIQUE_KEY,
    StructureCharacterisationDefinitions.UNIQUE.name: StructureCharacterisationDefinitions.UNIQUE,
}
