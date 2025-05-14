from dataclasses import dataclass
from typing import List, Optional

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FieldFunctionParameterDefinition(NldDataClassMixIn):
    allowed_data_types: Optional[List[str]] = None


@dataclass
class FieldFunctionDefinition(NldDataClassMixIn):
    name: str
    output_data_type: str
    parameters: Optional[List[FieldFunctionParameterDefinition]] = None
