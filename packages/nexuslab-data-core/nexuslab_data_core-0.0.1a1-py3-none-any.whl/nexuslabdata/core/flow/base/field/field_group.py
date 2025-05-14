from dataclasses import dataclass
from typing import List, Optional

from nexuslabdata.core import Structure
from nexuslabdata.core.flow.base.field.field_rule import FieldRule
from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


class StdFlowTransformationFieldGroupNames(NldStrEnum):
    DEFAULT = "DEFAULT"


class FlowTransformationFieldGroupType(NldStrEnum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


@dataclass
class FlowTransformationFieldGroupModel(NldDataClassMixIn):
    name: str
    type: str
    filter_allowed: bool = False
    non_link_field_rule_allowed: bool = False


@dataclass
class FlowTransformationFieldGroup(NldDataClassMixIn):
    name: str
    model: FlowTransformationFieldGroupModel
    structure: Optional[Structure] = None
    field_rules: Optional[List[FieldRule]] = None

    @property
    def filter_allowed(self) -> bool:
        return self.model.filter_allowed

    @property
    def non_link_field_rule_allowed(self) -> bool:
        return self.model.non_link_field_rule_allowed

    # Structure methods
    def update_data_structure(self, structure: Structure) -> None:
        """
        Applies the current structure to this field group.
        Resets all the field rules

        Parameters
        -----------
            structure : the structure to apply to this transformation

        """
        self.structure = structure
        self.field_rules = []

    def remove_field(self, field_name: str) -> None:
        if self.structure is not None:
            if self.structure.get_field(field_name) is not None:
                self.structure.remove_field(field_name)
