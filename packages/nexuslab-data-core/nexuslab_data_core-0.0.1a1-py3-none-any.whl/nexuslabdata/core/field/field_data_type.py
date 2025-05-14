from dataclasses import dataclass
from typing import Tuple

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FieldDataType(NldDataClassMixIn):
    data_type: str = "STRING"
    length: int = 0
    precision: int = 0

    def as_tuple(self) -> Tuple[str, int, int]:
        return self.data_type, self.length, self.precision
