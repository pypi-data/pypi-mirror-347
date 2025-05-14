from dataclasses import dataclass
from enum import auto
from typing import Dict, List, Optional

from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class FieldCharacterisationType(NldNamedDataClassMixIn):
    name: str


@dataclass
class FieldCharacterisationDefinition(NldNamedDataClassMixIn):
    name: str
    description: str
    allowed_attributes: Optional[List[str]] = None
    applicable_to_single_field_per_structure: bool = True


class FieldCharacterisationDefinitionAttributesNames(NldStrEnum):
    """Default Field Characterisation Names"""

    ENFORCED = auto()


class FieldCharacterisationDefinitionNames(NldStrEnum):
    MANDATORY = "MANDATORY"
    UNIQUE = "UNIQUE"

    REC_PREVIOUS_LAYER_UPDATE_TST = "REC_PREVIOUS_LAYER_UPDATE_TST"
    REC_INSERT_TST = "REC_INSERT_TST"
    REC_LAST_UPDATE_TST = "REC_LAST_UPDATE_TST"

    REC_SOURCE_EXTRACTION_TST = "REC_SOURCE_EXTRACTION_TST"
    REC_SOURCE_INSERT_TST = "REC_SOURCE_INSERT_TST"
    REC_SOURCE_LAST_UPDATE_TST = "REC_SOURCE_LAST_UPDATE_TST"

    REC_DELETION_FLAG = "REC_DELETION_FLAG"
    REC_DELETION_TST = "REC_DELETION_TST"
    REC_DELETION_USER_NAME = "REC_DELETION_USER_NAME"


class FieldCharacterisationDefinitions:
    """Field Characterisation common definitions"""

    """Generic constraints"""
    MANDATORY = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.MANDATORY.name,
        description="Field is mandatory",
        allowed_attributes=[
            FieldCharacterisationDefinitionAttributesNames.ENFORCED
        ],
        applicable_to_single_field_per_structure=False,
    )
    UNIQUE = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.UNIQUE.name,
        description="Content of the field is unique",
        allowed_attributes=[
            FieldCharacterisationDefinitionAttributesNames.ENFORCED
        ],
        applicable_to_single_field_per_structure=False,
    )

    """Record Technical Characterisations - General information on structure data changes"""
    REC_INSERT_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_INSERT_TST.name,
        description="Record Technical Characterisation - Timestamp of first insertion in the current structure",
        applicable_to_single_field_per_structure=True,
    )
    REC_INSERT_USER_NAME = auto()
    REC_LAST_UPDATE_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_LAST_UPDATE_TST.name,
        description="Record Technical Characterisation - Timestamp of last update in the current structure",
        applicable_to_single_field_per_structure=True,
    )
    REC_LAST_UPDATE_USER_NAME = auto()
    """ Record Technical Characterisations - Logical deletion flag """
    REC_DELETION_FLAG = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_DELETION_FLAG.name,
        description="Record Technical Characterisation - Deletion Flag (1 means logically deleted, 0 means active)",
        applicable_to_single_field_per_structure=True,
    )
    REC_DELETION_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_DELETION_TST.name,
        description="Record Technical Characterisation - Timestamp of the deletion in the current structure",
        applicable_to_single_field_per_structure=True,
    )
    REC_DELETION_USER_NAME = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_DELETION_USER_NAME.name,
        description="Record Technical Characterisation - User that applied the deletion in the current structure",
        applicable_to_single_field_per_structure=True,
    )
    """ Record Technical Characterisations - Logical archival flag """
    REC_ARCHIVE_FLAG = auto()
    REC_ARCHIVE_TST = auto()
    REC_ARCHIVE_USER_NAME = auto()

    """ Record Technical Characterisations - General Source information (insert, update, deletion 
    and archival information) """
    REC_SOURCE_INSERT_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_SOURCE_INSERT_TST.name,
        description="Record Technical Characterisation - Timestamp of first insertion in source structure",
        allowed_attributes=[],
        applicable_to_single_field_per_structure=True,
    )
    REC_SOURCE_INSERT_USER_NAME = auto()
    REC_SOURCE_LAST_UPDATE_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_SOURCE_LAST_UPDATE_TST.name,
        description="Record Technical Characterisation - Timestamp of last update in source structure",
        allowed_attributes=[],
        applicable_to_single_field_per_structure=True,
    )
    REC_SOURCE_LAST_UPDATE_USER_NAME = auto()
    REC_SOURCE_EXTRACTION_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_SOURCE_EXTRACTION_TST.name,
        description="Record Technical Characterisation - Timestamp of the extraction from the source",
        allowed_attributes=[],
        applicable_to_single_field_per_structure=True,
    )
    REC_PREVIOUS_LAYER_UPDATE_TST = FieldCharacterisationDefinition(
        name=FieldCharacterisationDefinitionNames.REC_PREVIOUS_LAYER_UPDATE_TST.name,
        description="Record Technical Characterisation - Timestamp of last update in the previous layer",
        allowed_attributes=[],
        applicable_to_single_field_per_structure=True,
    )
    REC_PREVIOUS_LAYER_UPDATE_USER_NAME = auto()
    REC_SOURCE_DELETION_FLAG = auto()
    REC_SOURCE_DELETION_TST = auto()
    REC_SOURCE_ARCHIVE_FLAG = auto()
    REC_SOURCE_ARCHIVE_TST = auto()
    """ Record Technical Characterisations - Specific Source information """
    """ Master Source characterisations define the source record information only for the master source structure 
    This is pertinent when there are multiple sources joined """
    REC_MASTER_SOURCE_INSERT_TST = auto()
    REC_MASTER_SOURCE_LAST_UPDATE_TST = auto()
    REC_MASTER_SOURCE_EXTRACTION_TST = auto()


# TODO: Remove this dictionary and replace with the dictionary of the enum of definitions
FIELD_CHARACTERISATION_DEFINITIONS: Dict[
    str, FieldCharacterisationDefinition
] = {
    FieldCharacterisationDefinitions.MANDATORY.name: FieldCharacterisationDefinitions.MANDATORY,
    FieldCharacterisationDefinitions.UNIQUE.name: FieldCharacterisationDefinitions.UNIQUE,
    FieldCharacterisationDefinitions.REC_INSERT_TST.name: FieldCharacterisationDefinitions.REC_INSERT_TST,
}
