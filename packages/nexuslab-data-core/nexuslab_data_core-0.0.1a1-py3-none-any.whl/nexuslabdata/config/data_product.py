from dataclasses import dataclass, field
from typing import Dict, Optional

from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class DataLayer(NldNamedDataClassMixIn):
    connection_name: str


@dataclass
class DataProduct(NldNamedDataClassMixIn):
    description: str
    version: Optional[str]
    layers: Dict[str, DataLayer] = field(default_factory=dict)
