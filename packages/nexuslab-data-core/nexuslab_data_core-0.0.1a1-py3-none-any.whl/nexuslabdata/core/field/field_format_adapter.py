from dataclasses import dataclass, field
from typing import Final, List, Optional, Tuple

from nexuslabdata.core.field.field_data_type import FieldDataType
from nexuslabdata.utils.data_class_mixin import (
    NldDataClassMixIn,
    NldNamedDataClassMixIn,
)

DEFAULT_DATA_TYPE_FOR_STRING: Final[FieldDataType] = FieldDataType(
    "STRING", 256, 0
)


@dataclass
class FieldFormatAdaptionRule(NldDataClassMixIn):
    """
    Field Format Adaptation rule

    This defines an adaptation rule for a field
    """

    allowed_data_types: List[str] = field(default_factory=list)
    allowed_characterisations: List[str] = field(default_factory=list)
    target_data_type: str = "STRING"
    length_rule: str = "0"
    precision_rule: str = "0"

    def _all_characterisations_allowed(self) -> bool:
        return len(self.allowed_characterisations) == 0

    def is_rule_applicable(
        self, data_type: str, field_characterisation_names: Optional[List[str]]
    ) -> bool:
        if data_type is None:
            return False
        characterisations_lcl = (
            field_characterisation_names
            if field_characterisation_names is not None
            else []
        )
        if data_type in self.allowed_data_types:
            if self._all_characterisations_allowed():
                return True
            else:
                if any(
                    char in self.allowed_characterisations
                    for char in characterisations_lcl
                ):
                    return True
        return False

    def get_adapted_field_format(
        self,
        data_type: str,
        length: Optional[int] = None,
        precision: Optional[int] = None,
    ) -> Tuple[str, int, int]:
        new_data_type = self.target_data_type
        new_length = int(
            self.length_rule.format(
                data_type=data_type, length=length, precision=precision
            )
        )
        new_precision = int(
            self.precision_rule.format(
                data_type=data_type, length=length, precision=precision
            )
        )
        return new_data_type, new_length, new_precision


@dataclass
class FieldFormatAdapter(NldNamedDataClassMixIn):
    rules: List[FieldFormatAdaptionRule] = field(default_factory=list)
    default_format: Optional[FieldDataType] = None
    default_keep_source_format: bool = True

    def get_adapted_field_format(
        self,
        data_type: str,
        length: Optional[int] = None,
        precision: Optional[int] = None,
        characterisations: Optional[List[str]] = None,
    ) -> Tuple[str, int, int]:
        for rule in self.rules:
            if rule.is_rule_applicable(
                data_type=data_type,
                field_characterisation_names=characterisations,
            ):
                return rule.get_adapted_field_format(
                    data_type, length, precision
                )
        return (
            (
                self.default_format.as_tuple()
                if self.default_format is not None
                else DEFAULT_DATA_TYPE_FOR_STRING.as_tuple()
            )
            if (not self.default_keep_source_format)
            else (data_type, length or 0, precision or 0)
        )
