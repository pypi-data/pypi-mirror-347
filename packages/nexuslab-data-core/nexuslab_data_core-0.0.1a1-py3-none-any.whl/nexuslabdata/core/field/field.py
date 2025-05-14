from dataclasses import dataclass
from typing import List, Optional, Union, cast

from nexuslabdata.core.events import FieldCharacterisationAlreadySet
from nexuslabdata.core.field.field_characterisation import FieldCharacterisation
from nexuslabdata.core.field.field_characterisation_def import (
    FieldCharacterisationDefinitionNames,
)
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class Field(NldNamedDataClassMixIn):
    desc: Optional[str] = None
    position: int = 0
    data_type: str = ""
    length: int = 0
    precision: int = 0
    default_value: Optional[Union[str | int]] = None
    characterisations: Optional[List[FieldCharacterisation]] = None

    def __post_init__(self) -> None:
        self._init_logger()

    # Characterisation methods
    def get_characterisations(self) -> List[FieldCharacterisation]:
        return (
            self.characterisations if self.characterisations is not None else []
        )

    def get_characterisation_names(self) -> List[str]:
        return [char.name for char in self.get_characterisations()]

    def get_characterisation(
        self, char: str
    ) -> Optional[FieldCharacterisation]:
        for char_lcl in self.get_characterisations():
            if char_lcl.name == char:
                return char_lcl
        return None

    def has_characterisations(self) -> bool:
        """
        Checks if this field has any characterisations

        Returns
        -----------
            True if this field has any characterisations

        """
        return (
            self.characterisations is not None
            and len(self.characterisations) > 0
        )

    def has_characterisation(self, char: str) -> bool:
        """
        Checks if this field has the requested characterisation

        Parameters
        -----------
            char : the characterisation to look for

        Returns
        -----------
            True if this field has the characterisation searched
        """
        return char in self.get_characterisation_names()

    def has_one_of_characterisations(
        self, characterisation_names: List[str]
    ) -> bool:
        """
        Checks if this field has one of the requested characterisation

        Parameters
        -----------
            characterisation_names : the list of characterisation names to look for

        Returns
        -----------
            True if this field has at least one of the characterisation names searched
        """
        return any(
            char in characterisation_names
            for char in self.get_characterisation_names()
        )

    def add_characterisation(
        self, new_char: Union[str | FieldCharacterisation]
    ) -> None:
        """
        Adds the characterisation provided in the characterisations of the field, if it does not already exist.
        The attributes are set to an empty dictionary

        Parameters
        -----------
            new_char : the characterisation to be added
        """
        char_to_add = (
            new_char
            if type(new_char) is FieldCharacterisation
            else FieldCharacterisation(name=cast(str, new_char))
        )
        self._add_characterisation(char_to_add)

    def _add_characterisation(self, new_char: FieldCharacterisation) -> None:
        """
        Adds the characterisation provided in the characterisations of the field, if it does not already exist

        Parameters
        -----------
            new_char : the characterisation to be added
        """
        if self.has_characterisation(new_char.name):
            self.log_event(
                FieldCharacterisationAlreadySet(self.name, new_char.name)
            )
            return
        if self.characterisations is None:
            self.characterisations = []
        self.characterisations.append(new_char)

    def remove_characterisation(self, name: str) -> None:
        """
        Removes the characterisation provided in the characterisations of the field, if it already exists

        Parameters
        -----------
            name : the characterisation to be removed
        """
        if name is not None:
            if name in self.get_characterisation_names():
                char_to_remove = None
                assert isinstance(self.characterisations, list)
                for char_lcl in self.characterisations:
                    if char_lcl.name == name:
                        char_to_remove = char_lcl
                        break
                if char_to_remove is not None:
                    self.characterisations.remove(char_to_remove)

    # Standard field characterisation methods
    def is_mandatory(self) -> bool:
        return self.has_characterisation(
            FieldCharacterisationDefinitionNames.MANDATORY
        )

    def set_mandatory(self) -> None:
        self.add_characterisation(
            FieldCharacterisationDefinitionNames.MANDATORY
        )

    def unset_mandatory(self) -> None:
        self.remove_characterisation(
            FieldCharacterisationDefinitionNames.MANDATORY
        )

    def is_unique(self) -> bool:
        return self.has_characterisation(
            FieldCharacterisationDefinitionNames.UNIQUE
        )

    def set_unique(self) -> None:
        self.add_characterisation(FieldCharacterisationDefinitionNames.UNIQUE)

    def unset_unique(self) -> None:
        self.remove_characterisation(
            FieldCharacterisationDefinitionNames.UNIQUE
        )

    def is_last_update_tst(self) -> bool:
        return self.has_characterisation(
            FieldCharacterisationDefinitionNames.REC_LAST_UPDATE_TST
        )

    def is_insert_tst(self) -> bool:
        return self.has_characterisation(
            FieldCharacterisationDefinitionNames.REC_INSERT_TST
        )

    def is_source_last_update_tst(self) -> bool:
        return self.has_characterisation(
            FieldCharacterisationDefinitionNames.REC_SOURCE_LAST_UPDATE_TST
        )
