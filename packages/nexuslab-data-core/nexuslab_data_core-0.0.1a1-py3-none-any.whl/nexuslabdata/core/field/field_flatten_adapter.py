from typing import Optional, Tuple

from nexuslabdata.core.field.field import Field
from nexuslabdata.core.field.field_characterisation import FieldCharacterisation
from nexuslabdata.utils.data_class_flatten_adapter import (
    DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL,
    ObjectFlattenAdapter,
)


class FieldFlattenAdapter(ObjectFlattenAdapter[Field]):
    @classmethod
    def flatten(cls, field: Field) -> Tuple[Optional[str | int], ...]:
        field_tuple = (
            field.name,
            field.desc,
            field.position,
            field.data_type,
            field.length,
            field.precision,
            field.default_value,
            DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL.join(
                [
                    cls.flatten_field_characterisation(field_characterisation)
                    for field_characterisation in field.get_characterisations()
                ]
            )
            if field.has_characterisations()
            else None,
        )
        return field_tuple

    @classmethod
    def flatten_field_characterisation(
        cls, field_characterisation: FieldCharacterisation
    ) -> str:
        if not field_characterisation.has_attributes():
            attribute_str = ""
        else:
            dict_as_string = cls._flatten_in_single_cell_dict(
                field_characterisation.attributes
            )
            attribute_str = (
                f"({dict_as_string})"
                if dict_as_string is not None and len(dict_as_string) > 0
                else ""
            )
        return f"{field_characterisation.name}{attribute_str}"
