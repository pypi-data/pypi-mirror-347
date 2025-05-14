from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, cast

from nexuslabdata.core import FieldCharacterisationDefinitionNames
from nexuslabdata.core.events import (
    FieldAdditionInvalidPosition,
    NotAvailableFieldInStructure,
)
from nexuslabdata.core.exceptions import (
    FieldAdditionException,
    FieldRemovalException,
    NotAvailableFieldException,
)
from nexuslabdata.core.field import Field
from nexuslabdata.core.structure.structure_characterisation import (
    StructureCharacterisation,
)
from nexuslabdata.core.structure.structure_characterisation_def import (
    STRUCTURE_CHARACTERISATION_DEFINITIONS,
    StructureCharacterisationDefinition,
    StructureCharacterisationDefinitionNames,
)
from nexuslabdata.exceptions import (
    MissingMandatoryArgumentException,
    NldRuntimeException,
)
from nexuslabdata.logging.events import MissingMandatoryArgument
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class Structure(NldNamedDataClassMixIn):
    type: str
    row_count: int = 0
    desc: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    fields: List[Field] = field(default_factory=list)
    characterisations: Optional[List[StructureCharacterisation]] = None

    # Structure-level methods
    def is_table(self) -> bool:
        """
        Checks if the structure is a table.
        Accepted values for structure type are : BASE TABLE and TABLE

        Returns
        -----------
            True, if the structure is a table
            False, otherwise
        """
        return (
            self.type.upper() in ["BASE TABLE", "TABLE"]
            if self.type is not None
            else False
        )

    def is_view(self) -> bool:
        """
        Checks if the structure is a view.
        Accepted values for structure type are : VIEW

        Returns
        -----------
            True, if the structure is a view
            False, otherwise
        """
        return self.type.upper() in ["VIEW"] if self.type is not None else False

    # Field-level methods
    def get_fields(self) -> List[Field]:
        return self.fields

    def get_field_names(self) -> List[str]:
        """
        Get the list of field names by ordinal position

        Returns
        -----------
            The list of the field names
        """
        self.sort_fields_by_ordinal_position()
        return [field.name for field in self.fields]

    def get_field(self, name: str) -> Field:
        """
        Get a field based on its name
        Returns an exception if the field is not available

        Parameters
        -----------
            The field name to look for

        Returns
        -----------
            The field structure with the provided field name
        """
        for field in self.fields:
            if field.name == name:
                return field
        self.log_event(NotAvailableFieldInStructure(self.name, name))
        raise NotAvailableFieldException(
            structure_name=self.name, field_name=name
        )

    def has_field(self, name: str) -> bool:
        """
        Checks if a field with the provided name is available in the structure

        Parameters
        -----------
            The field name to look for

        Returns
        -----------
            True, if a field with the provided name exists
        """
        for field in self.fields:
            if field.name == name:
                return True
        return False

    def get_fields_based_on_names(self, field_names: List[str]) -> List[Field]:
        return [self.get_field(field_name) for field_name in field_names]

    def get_single_field_with_characterisation_name(
        self, characterisation_name: str
    ) -> Optional[Field]:
        """
        Get a single field with the characterisation name provided

        Parameters
        -----------
            characterisation_name : The characterisation name to look for

        Returns
        -----------
            The first found field with the provided field characterisation name.
            If none found, None is returned
        """
        found_fields = self.get_fields_with_characterisation_name(
            characterisation_name
        )
        if len(found_fields) == 0:
            return None
        selected_field = found_fields[0]
        if len(found_fields) > 1:
            self.log_warn(
                f"Multiple fields with characterisation {characterisation_name} found in "
                f'structure {self.name} : {", ".join([field.name for field in found_fields])}'
            )
            self.log_warn(
                f"First field will be selected : {selected_field.name}"
            )
            return selected_field
        return selected_field

    def get_fields_with_characterisation_name(
        self, characterisation_name: str
    ) -> List[Field]:
        """
        Get the list of field with the provided characterisation name

        Parameters
        -----------
            characterisation_name : The characterisation name to look for

        Returns
        -----------
            The list of field with the provided characterisation
        """
        return [
            field
            for field in self.fields
            if field.has_characterisation(characterisation_name)
        ]

    def has_field_with_characterisation_name(
        self, characterisation_name: str
    ) -> bool:
        """
        Check that at least one field in this structure has one field with the provided characterisation name

        Parameters
        -----------
            characterisation_name : The characterisation name to look for

        Returns
        -----------
            True, if there is at least one field with the provided characterisation
        """
        return (
            len(
                self.get_fields_with_characterisation_name(
                    characterisation_name
                )
            )
            > 0
        )

    def get_fields_with_characterisation_names(
        self, characterisation_names: List[str]
    ) -> List[Field]:
        """
        Get the list of field with any of the provided characterisations

        Parameters
        -----------
            characterisation_names : The list of characterisation names to look for

        Returns
        -----------
            The list of field with the provided characterisation
        """
        return [
            field
            for field in self.fields
            if any(
                char in characterisation_names
                for char in [
                    char.name for char in field.get_characterisations()
                ]
            )
        ]

    def has_field_with_one_of_characterisation_names(
        self, characterisation_names: List[str]
    ) -> bool:
        """
        Check that at least one field in this structure has one field with at least one of the provided
        characterisation names

        Parameters
        -----------
            characterisation_names : The list of characterisation names to look for

        Returns
        -----------
            True, if there is at least one field with one of the provided characterisations
        """
        return (
            len(
                self.get_fields_with_characterisation_names(
                    characterisation_names
                )
            )
            > 0
        )

    def get_fields_wo_characterisation_names(
        self, characterisation_names: List[str]
    ) -> List[Field]:
        """
        Get the list of field without any of the provided characterisation names

        Parameters
        -----------
            characterisation_names : The list of characterisation names to look for

        Returns
        -----------
            The list of field without any of the provided characterisation names
        """
        return [
            field
            for field in self.fields
            if field
            not in self.get_fields_with_characterisation_names(
                characterisation_names
            )
        ]

    def get_field_names_with_characterisation_name(
        self, characterisation_name: str
    ) -> List[str]:
        """
        Get the list of field names with the provided characterisation

        Parameters
        -----------
            characterisation_name : The characterisation to look for

        Returns
        -----------
            The list of field names with the provided characterisation
        """
        return [
            field.name
            for field in self.get_fields_with_characterisation_name(
                characterisation_name
            )
        ]

    def get_field_names_with_characterisation_names(
        self, characterisation_names: list[str]
    ) -> List[str]:
        """
        Get the list of field names with any of the provided characterisation names

        Parameters
        -----------
            characterisation_names : The list of characterisation names to look for

        Returns
        -----------
            The list of field names with the provided characterisation names
        """
        return [
            field.name
            for field in self.get_fields_with_characterisation_names(
                characterisation_names
            )
        ]

    def get_field_names_wo_characterisation_names(
        self, characterisation_names: list[str]
    ) -> List[str]:
        """
        Get the list of field names without any of the provided characterisations

        Parameters
        -----------
            characterisation_names : The list of characterisation names to look for

        Returns
        -----------
            The list of field names without any of the provided characterisation names
        """
        return [
            field.name
            for field in self.get_fields_wo_characterisation_names(
                characterisation_names
            )
        ]

    def add_field(
        self,
        new_field: Field,
        force_position: bool = False,
        prevent_position_check: bool = False,
        previous_field_name: Optional[str] = None,
        next_field_name: Optional[str] = None,
    ) -> None:
        """
        Adds the provided field to this structure

        The field can be provided with a predefined position, or without a position.
        If the field has a predefined position, this value is checked to be equal to the current number of fields plus 1
        , as this field is by default added as the last field of the structure

        Parameters
        -----------
            new_field : The new field to be added
            force_position : Flag to force the position stored in the new field to be taken into account
                The force_position takes priority over prevent_position_check argument and over the
                previous_field_name and next_field_name arguments, e.g. if force_position is True
                , the position of the field is forced based on the position valued in the field provided
                and all the fields in the structure are modified accordingly and all other parameters are
                not used.
            prevent_position_check: Flag to prevent any position check while adding the fields
            previous_field_name : The previous field name, when field is to be added after a specific field
            next_field_name : The next field name, when field is to be added before a specific field

        """
        if new_field is None:
            self.log_event(
                MissingMandatoryArgument(
                    method_name="Add Field",
                    object_type=type(self),
                    argument_name="New Field",
                )
            )
            raise MissingMandatoryArgumentException(
                method_name="Add Field",
                object_type=type(self),
                argument_name="New Field",
            )

        if force_position:
            pos_to_add_new_field = new_field.position

            for field in self.fields:
                if field.position >= pos_to_add_new_field:
                    field.position = field.position + 1
            self.fields.append(new_field)

        elif (previous_field_name is None) & (next_field_name is None):
            if not prevent_position_check:
                if (new_field.position is None) | (new_field.position == 0):
                    new_field.position = len(self.fields) + 1
                elif new_field.position != (len(self.fields) + 1):
                    self.log_event(
                        FieldAdditionInvalidPosition(
                            field_name=new_field.name,
                            structure_name=self.name,
                            position=new_field.position,
                            expected_last_position=len(self.fields) + 1,
                        )
                    )
                    raise FieldAdditionException(
                        field_name=new_field.name, structure_name=self.name
                    )

            self.fields.append(new_field)

        else:
            if previous_field_name is not None:
                field = self.get_field(previous_field_name)
                if field is None:
                    self.log_event(
                        NotAvailableFieldInStructure(
                            field_name=previous_field_name,
                            structure_name=self.name,
                        )
                    )
                    raise FieldAdditionException(
                        field_name=new_field.name, structure_name=self.name
                    )

                pos_to_add_new_field = field.position + 1
            elif next_field_name is not None:
                field = self.get_field(next_field_name)
                if field is None:
                    self.log_event(
                        NotAvailableFieldInStructure(
                            field_name=next_field_name, structure_name=self.name
                        )
                    )
                    raise FieldAdditionException(
                        field_name=new_field.name, structure_name=self.name
                    )
                pos_to_add_new_field = field.position

            for field in self.fields:
                if field.position >= pos_to_add_new_field:
                    field.position += 1
            new_field.position = pos_to_add_new_field
            self.fields.append(new_field)

    def remove_field(self, name: str) -> None:
        """
        Removes the field with the provided name and updates all the position values of the fields contained in this structure

        Parameters
        -----------
            name : The new field to be removed

        """
        field_to_remove = self.get_field(name)
        if field_to_remove is None:
            self.log_event(
                NotAvailableFieldInStructure(
                    field_name=name, structure_name=self.name
                )
            )
            raise FieldRemovalException(
                field_name=name, structure_name=self.name
            )
        base_position = field_to_remove.position
        self.fields.remove(field_to_remove)
        for field in self.fields:
            if field.position > base_position:
                field.position -= 1

    def remove_fields(self, names: List[str]) -> None:
        """
        Removes the fields with the provided names and updates all the position values of the fields contained in this structure.

        Parameters
        -----------
            names : The list of fields to be removed

        """
        for name in names:
            self.remove_field(name)

    def sort_fields_by_ordinal_position(self) -> None:
        """
        Sort the Fields by Ordinal Position
        """
        self.fields = sorted(self.fields, key=lambda field: field.position)

    def get_number_of_fields(self) -> int:
        """
        Get the number of fields contained in the data structure definition

        Returns
        -----------
            The number of fields
        """
        return len(self.fields)

    # Field Characterisation related methods
    def _get_fields_associated_to_unique_structure_characterisation(
        self, characterisation_name: str
    ) -> List[Field]:
        if not self.has_characterisation_with_definition(characterisation_name):
            return []
        structure_characterisation = (
            self.get_characterisation_with_definition_name(
                characterisation_name
            )
        )
        if structure_characterisation is None:
            return []
        field_names = structure_characterisation.linked_fields
        return (
            self.get_fields_based_on_names(field_names)
            if field_names is not None
            else []
        )

    def has_tec_unique_key(self) -> bool:
        """
        Check if this structure has a technical key.

        A structure has a functional if at least 1 field is part of the technical key.

        Returns
        -----------
            True, if the structure has a technical key
        """
        return len(self.get_tec_unique_key_fields()) > 0

    def get_tec_unique_key_fields(self) -> List[Field]:
        """
        Get the list of fields contained in the structure technical key

        Returns
        -----------
            The fields contained in the structure technical key
        """
        return self._get_fields_associated_to_unique_structure_characterisation(
            StructureCharacterisationDefinitionNames.TECHNICAL_UNIQUE_KEY
        )

    def has_functional_unique_key(self) -> bool:
        """
        Check if this structure has a functional unique key.

        A structure has a functional if at least 1 field is part of the functional unique key.

        Returns
        -----------
            True, if the structure has a functional unique key
        """
        return len(self.get_functional_unique_key_fields()) > 0

    def get_functional_unique_key_fields(self) -> List[Field]:
        """
        Get the list of fields contained in the structure functional key

        Returns
        -----------
            The fields contained in the structure functional key
        """
        return self._get_fields_associated_to_unique_structure_characterisation(
            StructureCharacterisationDefinitionNames.FUNCTIONAL_UNIQUE_KEY
        )

    def get_last_update_tst_field(self) -> Optional[Field]:
        """
        Get the last update timestamp field.
        If there are multiple last update timestamp fields in this structure, a warning message is logged and one of
        the fields is returned (randomly)

        Returns
        -----------
            The last update timestamp field.
        """
        return self.get_single_field_with_characterisation_name(
            FieldCharacterisationDefinitionNames.REC_LAST_UPDATE_TST
        )

    def get_insert_tst_field(self) -> Optional[Field]:
        """
        Get the insert timestamp field.
        If there are multiple insert timestamp fields in this structure, a warning message is logged and one of
        the fields is returned (randomly)

        Returns
        -----------
            The last update timestamp field.
        """
        return self.get_single_field_with_characterisation_name(
            FieldCharacterisationDefinitionNames.REC_INSERT_TST
        )

    def get_source_last_update_tst_field(self) -> Optional[Field]:
        """
        Get the source last update timestamp field.
        If there are multiple source last update timestamp fields in this structure, a warning message is logged and
        one of the fields is returned (randomly)

        Returns
        -----------
            The last update timestamp field.
        """
        return self.get_single_field_with_characterisation_name(
            FieldCharacterisationDefinitionNames.REC_SOURCE_LAST_UPDATE_TST
        )

    # Options methods
    def get_options(self) -> Dict[str, Any]:
        """
        Get the options dictionary

        Returns
        -------
            The options dictionary
        """
        return self.options if self.options is not None else {}

    def get_option_keys(self) -> List[str]:
        """
        Get the available option keys

        Returns
        -------
            The list of options keys
        """
        return list(self.get_options().keys())

    def has_option(self, key: str) -> bool:
        """
        Checks if this structure has the provided option key

        Parameters
        ----------
        key : str
            The option key

        Returns
        -------
            True if an option with this key is available
        """
        return key in self.get_option_keys()

    def get_option_value(self, key: str) -> Any:
        """
        Get the option value for the provided key

        Parameters
        ----------
        key : str
            The option key

        Returns
        -------
            The option value
        """
        return self.get_options().get(key)

    # Characterisation methods
    def get_characterisations(
        self,
    ) -> List[StructureCharacterisation]:
        return (
            self.characterisations if self.characterisations is not None else []
        )

    def get_characterisation_definition_names(
        self,
    ) -> List[str]:
        return [char.definition_name for char in self.get_characterisations()]

    def get_characterisation_with_definition_name(
        self, definition_name: str
    ) -> Optional[StructureCharacterisation]:
        for char in self.get_characterisations():
            if char.definition_name == definition_name:
                return char
        return None

    def get_characterisations_with_definition_name(
        self, definition_name: str
    ) -> List[StructureCharacterisation]:
        return [
            char
            for char in self.get_characterisations()
            if char.definition_name == definition_name
        ]

    def has_characterisations(self) -> bool:
        """
        Checks if this structure has any characterisations

        Returns
        -----------
            True if this structure has any characterisations

        """
        return len(self.get_characterisations()) > 0

    def has_characterisation_with_definition(
        self, definition_name: str
    ) -> bool:
        """
        Checks if this structure has a characterisation with the provided definition name

        Parameters
        -----------
            definition_name : the characterisation definition name to look for

        Returns
        -----------
            True if this structure has a characterisation with the provided definition name
        """
        return definition_name in self.get_characterisation_definition_names()

    def has_any_characterisation_with_definition(
        self, definition_names: List[str]
    ) -> bool:
        """
        Checks if this structure has any of the requested characterisation definition names

        Parameters
        -----------
            definition_names : the list of characterisation definition names to look for

        Returns
        -----------
            True if this structure has at least one of the characterisation definition names
        """
        return any(
            char in self.get_characterisation_definition_names()
            for char in definition_names
        )

    def get_matching_characterisation_definition_names(
        self, definition_names: List[str]
    ) -> List[str]:
        """
        Checks all the matching characterisations from the provided list with this structure charactersations

        Parameters
        -----------
            definition_names : the list of characterisations to look for

        Returns
        -----------
            A list of the matching characterisations
        """
        return [
            char
            for char in definition_names
            if self.has_characterisation_with_definition(char)
        ]

    def add_characterisation(
        self, structure_characterisation: StructureCharacterisation
    ) -> None:
        """
        Adds the characterisation provided in the characterisations of the structure

        Parameters
        -----------
            structure_characterisation : the structure characterisation to be added
        """
        definition_name = structure_characterisation.definition_name
        name = structure_characterisation.name
        if self.has_characterisation_with_definition(definition_name):
            if not cast(
                StructureCharacterisationDefinition,
                STRUCTURE_CHARACTERISATION_DEFINITIONS.get(definition_name),
            ).allowed_multiple_characterisations_per_structure:
                self.log_error(
                    f"Characterisation {definition_name} with name {name} is already present in structure {self.name}"
                )
                raise NldRuntimeException(
                    msg=f"Characterisation {definition_name} with name {name} is already present in structure {self.name}"
                )
        if self.characterisations is None:
            self.characterisations = []
        self.characterisations.append(structure_characterisation)

    def add_characterisation_with_name_only(
        self, definition_name: str, name: str
    ) -> None:
        """
        Adds the characterisation provided in the characterisations of the structure
        If characterisation already exists, an exception is thrown

        Parameters
        -----------
            definition_name : the characterisation definition name
            name : the characterisation name
        """
        self.add_characterisation(
            StructureCharacterisation(
                definition_name=definition_name, name=name
            )
        )

    def remove_characterisation_based_on_definition_name(
        self, definition_name: str
    ) -> None:
        """
        Removes the characterisation equal to the provided definition name

        Parameters
        -----------
            definition_name : the characterisation definition name to be removed
        """
        if self.characterisations is None:
            return
        for char in self.characterisations:
            if char.definition_name == definition_name:
                self.characterisations.remove(char)
