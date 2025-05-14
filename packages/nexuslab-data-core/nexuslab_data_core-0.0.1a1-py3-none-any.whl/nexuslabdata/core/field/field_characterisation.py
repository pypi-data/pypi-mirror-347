from dataclasses import dataclass
from typing import Dict, Optional

from nexuslabdata.core.field.field_characterisation_def import (
    FieldCharacterisationDefinition,
)
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class FieldCharacterisation(NldNamedDataClassMixIn):
    name: str
    attributes: Optional[Dict[str, str]] = None

    def has_attributes(self) -> bool:
        return self.attributes is not None and len(self.attributes) > 0

    @classmethod
    def create_from_definition(
        cls, definition: FieldCharacterisationDefinition
    ) -> "FieldCharacterisation":
        return FieldCharacterisation(name=definition.name)
