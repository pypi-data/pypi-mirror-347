from dataclasses import dataclass
from typing import Optional

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FieldCharacterisationMapping(NldDataClassMixIn):
    characterisation: str
    src_characterisation: Optional[str] = None
    rule: Optional[str] = None
    default_value: Optional[str] = None

    def has_src_char(self) -> bool:
        return self.src_characterisation is not None
