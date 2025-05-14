from dataclasses import dataclass
from typing import Hashable, Optional

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class StructureNamespace(NldDataClassMixIn, Hashable):
    databank: str
    catalog: Optional[str]
    namespace: Optional[str]

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.as_dict() == other.as_dict()

    def __str__(self) -> str:
        return ".".join(
            [self.databank, self.catalog or "", self.namespace or ""]
        )
