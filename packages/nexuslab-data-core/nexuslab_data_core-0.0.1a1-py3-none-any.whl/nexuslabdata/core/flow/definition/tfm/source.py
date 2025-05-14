from dataclasses import dataclass
from typing import Optional

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FlowSourceDefinition(NldDataClassMixIn):
    name: str
    namespace: Optional[str] = None
