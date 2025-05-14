from typing import Any, Dict, List

from nexuslabdata.core.field.field import Field
from nexuslabdata.core.field.field_characterisation import FieldCharacterisation
from nexuslabdata.core.structure.structure import Structure
from nexuslabdata.core.structure.structure_characterisation import (
    StructureCharacterisation,
)
from nexuslabdata.core.structure.structure_flatten_adapter import (
    StructureFlattenAdapter,
)
from nexuslabdata.utils.csv_adapter import (
    CsvAdapter,
    CsvDataSchema,
    CsvRowDefinition,
)
from nexuslabdata.utils.data_class_flatten_adapter import (
    DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL,
)

STRUCTURE_CSV_DATA_SCHEMA = CsvDataSchema(
    row_type_column_position=0,
    row_types=[
        CsvRowDefinition(
            StructureFlattenAdapter.STRUCTURE_ROW_NAME,
            "self._create_structure_from_row(row)",
        ),
        CsvRowDefinition(
            StructureFlattenAdapter.STRUCTURE_CHARACTERISATION_ROW_NAME,
            "self._create_structure_characterisation_from_row(row)",
        ),
        CsvRowDefinition(
            StructureFlattenAdapter.FIELD_ROW_NAME,
            "self._create_field_from_row(row)",
        ),
    ],
    header_row_list=[
        "Row Type",
        "Structure Name",
        "|Definition Name|Field Name",
        "Description|Name|Field Description|",
        "Type|Linked Fields|Field Position",
        "Row Count|Attributes|Data Type",
        "Options||Length",
        "||Precision",
        "||Default Value",
        "||Characterisation",
        "",
        "",
    ],
    adapter=StructureFlattenAdapter,
)


class StructureCsvAdapter(CsvAdapter[Structure]):
    def __init__(self) -> None:
        super().__init__(csv_data_schema=STRUCTURE_CSV_DATA_SCHEMA)

    def _create_object_from_rows(
        self, object_dict: Dict[str, List[Any]]
    ) -> Structure:
        data_structure: Structure = object_dict[
            StructureFlattenAdapter.STRUCTURE_ROW_NAME
        ][0]
        structure_characterisations: List[StructureCharacterisation] = (
            object_dict[
                StructureFlattenAdapter.STRUCTURE_CHARACTERISATION_ROW_NAME
            ]
            if StructureFlattenAdapter.STRUCTURE_CHARACTERISATION_ROW_NAME
            in list(object_dict.keys())
            else []
        )
        fields: List[Field] = object_dict[
            StructureFlattenAdapter.FIELD_ROW_NAME
        ]
        for structure_characterisation in structure_characterisations:
            data_structure.add_characterisation(structure_characterisation)
        for field in fields:
            data_structure.add_field(new_field=field)
        return data_structure

    def _create_structure_from_row(self, row: List[str]) -> Structure:
        return Structure(
            name=row[1],
            desc=row[3],
            type=row[4],
            row_count=self._get_int_from_single_cell(row[5]) or 0,
            options=self._get_dict_from_str_single_cell(row[6]),
            fields=[],
            characterisations=[],
        )

    def _create_structure_characterisation_from_row(
        self, row: List[str]
    ) -> StructureCharacterisation:
        linked_fields_list = self._get_list_from_single_cell(
            row[4], delimiter=DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL
        )
        return StructureCharacterisation(
            definition_name=row[2],
            name=row[3],
            linked_fields=linked_fields_list,
        )

    def _create_field_from_row(self, row: List[str]) -> Field:
        characterisation_list = self._get_list_from_single_cell(
            row[9], delimiter=DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL
        )
        characterisations = []
        for characterisation in characterisation_list:
            (
                name,
                attributes,
            ) = self._get_tuple_for_name_attributes_from_str_single_cell(
                characterisation
            )
            characterisations.append(
                FieldCharacterisation(name=name, attributes=attributes)
            )

        return Field(
            name=row[2],
            desc=row[3],
            position=self._get_int_from_single_cell(row[4]) or 0,
            data_type=row[5],
            length=self._get_int_from_single_cell(row[6]) or 0,
            precision=self._get_int_from_single_cell(row[7]) or 0,
            default_value=row[8] if row[8] != "" else None,
            characterisations=characterisations,
        )
