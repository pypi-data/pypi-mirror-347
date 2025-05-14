from dataclasses import dataclass
from typing import Optional

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class TargetFromSourceMappingDefinition(NldDataClassMixIn):
    target_field_name: Optional[str] = None
    source_field_name: Optional[str] = None
    function_name: Optional[str] = None
    formula: Optional[str] = None
