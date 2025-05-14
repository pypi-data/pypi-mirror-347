from dataclasses import dataclass

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FieldFunction(NldDataClassMixIn):
    name: str
    formula: str
