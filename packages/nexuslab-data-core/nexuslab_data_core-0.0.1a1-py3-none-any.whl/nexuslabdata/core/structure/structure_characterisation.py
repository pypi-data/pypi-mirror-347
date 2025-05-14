from dataclasses import dataclass
from typing import Dict, List, Optional

from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class StructureCharacterisation(NldNamedDataClassMixIn):
    definition_name: str
    name: str
    linked_fields: Optional[List[str]] = None
    attributes: Optional[Dict[str, str]] = None
