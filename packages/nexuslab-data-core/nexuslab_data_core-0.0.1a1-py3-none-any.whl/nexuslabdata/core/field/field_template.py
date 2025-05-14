from dataclasses import dataclass
from typing import Optional

from nexuslabdata.core.field.field import Field
from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


class FieldTemplateRelativePosition(NldStrEnum):
    START = "START"
    END = "END"


@dataclass
class FieldTemplate(NldNamedDataClassMixIn):
    name: str
    field: Field
    override_existing_field_on_characterisation: Optional[str] = None
    relative_position: str = FieldTemplateRelativePosition.END

    def get_field_instance(self) -> Field:
        """
        Get a field instance for this field template

        Returns
        -----------
            A new field based on this template
        """
        return Field.deep_copy(self.field)
