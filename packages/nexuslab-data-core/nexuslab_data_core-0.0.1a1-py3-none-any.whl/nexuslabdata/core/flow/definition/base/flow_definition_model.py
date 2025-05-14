from dataclasses import dataclass
from typing import List, Optional

from nexuslabdata.core.flow.definition.field.field_characterisation_mapping import (
    FieldCharacterisationMapping,
)
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FlowDefinitionModel(NldDataClassMixIn):
    name: str
    target_structure_adapter_name: Optional[str] = None
    field_characterisation_mapping: Optional[
        List[FieldCharacterisationMapping]
    ] = None
    field_mapping_match_names: bool = True
    target_merge_characterisation_rule: Optional[str] = None
