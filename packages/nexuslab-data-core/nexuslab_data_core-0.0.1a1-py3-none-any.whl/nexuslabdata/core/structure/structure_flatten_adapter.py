from typing import List, Optional, Tuple, Union

from nexuslabdata.core.field.field_flatten_adapter import FieldFlattenAdapter
from nexuslabdata.core.structure.structure import Structure
from nexuslabdata.core.structure.structure_characterisation import (
    StructureCharacterisation,
)
from nexuslabdata.utils.data_class_flatten_adapter import (
    DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL,
    ListFlattenAdapter,
)


class StructureFlattenAdapter(ListFlattenAdapter[Structure]):
    STRUCTURE_ROW_NAME = "Structure"
    STRUCTURE_CHARACTERISATION_ROW_NAME = "Characterisation"
    FIELD_ROW_NAME = "Field"

    @classmethod
    def flatten(
        cls, structure: Structure
    ) -> List[Tuple[Optional[Union[int | str]], ...]]:
        flatten_structure: List[Tuple[Optional[int | str], ...]] = []
        structure_tuple = (
            cls.STRUCTURE_ROW_NAME,
            structure.name,
            None,
            structure.desc,
            structure.type,
            structure.row_count,
            cls._flatten_in_single_cell_dict(structure.options),
        )
        flatten_structure.append(structure_tuple)
        for structure_characterisation in structure.get_characterisations():
            flatten_structure_char = cls.flatten_structure_characterisation(
                structure_characterisation
            )
            flatten_structure.append(
                (cls.STRUCTURE_CHARACTERISATION_ROW_NAME, structure.name)
                + flatten_structure_char
            )
        for field in structure.get_fields():
            flatten_field = FieldFlattenAdapter.flatten(field)
            flatten_structure.append(
                (cls.FIELD_ROW_NAME, structure.name) + flatten_field
            )
        return flatten_structure

    @classmethod
    def flatten_structure_characterisation(
        cls, structure_characterisation: StructureCharacterisation
    ) -> Tuple[Optional[Union[int | str]], ...]:
        structure_characterisation_tuple = (
            structure_characterisation.definition_name,
            structure_characterisation.name,
            DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL.join(
                structure_characterisation.linked_fields
            )
            if structure_characterisation.linked_fields is not None
            else None,
            cls._flatten_in_single_cell_dict(
                structure_characterisation.attributes
            ),
        )
        return structure_characterisation_tuple
