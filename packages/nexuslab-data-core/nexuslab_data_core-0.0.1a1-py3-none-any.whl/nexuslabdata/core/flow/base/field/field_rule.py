from dataclasses import dataclass
from typing import List

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FieldRule(NldDataClassMixIn):
    field_name: str
    rule: str
    source_fields: List[str]

    def is_link(self) -> bool:
        return (not self.is_rule()) & (self.has_single_source())

    def is_rule(self) -> bool:
        return self.rule is not None

    def has_single_source(self) -> bool:
        return len(self.source_fields) == 1

    def get_source_field_name(self) -> str:
        if not self.has_single_source():
            raise ValueError(
                "Field rule does not have a single source field. "
                'The "get single source field" name method should not be called.'
            )
        return self.source_fields[0]
