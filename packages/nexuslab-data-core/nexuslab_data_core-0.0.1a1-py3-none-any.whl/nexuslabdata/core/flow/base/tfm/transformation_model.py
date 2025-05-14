from dataclasses import dataclass
from typing import List

from nexuslabdata.core.flow.base.field import FlowTransformationFieldGroupModel
from nexuslabdata.core.flow.base.field.field_group import (
    FlowTransformationFieldGroupType,
    StdFlowTransformationFieldGroupNames,
)
from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn

FIELD_GROUP_INFINITY_VALUE: int = 99


class StdFlowTransformationModelNames(NldStrEnum):
    SOURCE = "SOURCE"
    TARGET = "TARGET"
    STANDARD = "STANDARD"


@dataclass
class FlowTransformationModel(NldDataClassMixIn):
    name: str
    field_group_models: List[FlowTransformationFieldGroupModel]
    input_allowed: bool = True
    output_allowed: bool = True
    input_field_groups_allowed: int = 1
    output_field_groups_allowed: int = 1
    tfm_filter_allowed: bool = False
    input_field_group_filter_allowed: bool = False
    output_field_groups_filter_allowed: bool = False
    tfm_standard_structure: bool = False

    def has_unlimited_input_field_groups_allowed(self) -> bool:
        return self.input_field_groups_allowed == FIELD_GROUP_INFINITY_VALUE

    def has_unlimited_output_field_groups_allowed(self) -> bool:
        return self.output_field_groups_allowed == FIELD_GROUP_INFINITY_VALUE


FLOW_SOURCE_MODEL = FlowTransformationModel(
    name=StdFlowTransformationModelNames.SOURCE,
    field_group_models=[
        FlowTransformationFieldGroupModel(
            name=StdFlowTransformationFieldGroupNames.DEFAULT,
            type=FlowTransformationFieldGroupType.OUTPUT,
            filter_allowed=False,
            non_link_field_rule_allowed=False,
        )
    ],
    input_allowed=False,
    output_allowed=True,
    input_field_groups_allowed=0,
    output_field_groups_allowed=1,
    tfm_filter_allowed=False,
    input_field_group_filter_allowed=False,
    output_field_groups_filter_allowed=False,
    tfm_standard_structure=True,
)

FLOW_TARGET_MODEL = FlowTransformationModel(
    name=StdFlowTransformationModelNames.TARGET,
    field_group_models=[
        FlowTransformationFieldGroupModel(
            name=StdFlowTransformationFieldGroupNames.DEFAULT,
            type=FlowTransformationFieldGroupType.INPUT,
            filter_allowed=False,
            non_link_field_rule_allowed=False,
        )
    ],
    input_allowed=True,
    output_allowed=False,
    input_field_groups_allowed=1,
    output_field_groups_allowed=0,
    tfm_filter_allowed=False,
    input_field_group_filter_allowed=False,
    output_field_groups_filter_allowed=False,
    tfm_standard_structure=True,
)

FLOW_STANDARD_MODEL = FlowTransformationModel(
    name=StdFlowTransformationModelNames.STANDARD,
    field_group_models=[
        FlowTransformationFieldGroupModel(
            name=StdFlowTransformationFieldGroupNames.DEFAULT,
            type=FlowTransformationFieldGroupType.INPUT,
            filter_allowed=True,
            non_link_field_rule_allowed=True,
        ),
        FlowTransformationFieldGroupModel(
            name=StdFlowTransformationFieldGroupNames.DEFAULT,
            type=FlowTransformationFieldGroupType.OUTPUT,
            filter_allowed=True,
            non_link_field_rule_allowed=True,
        ),
    ],
    input_allowed=True,
    output_allowed=True,
    input_field_groups_allowed=FIELD_GROUP_INFINITY_VALUE,
    output_field_groups_allowed=FIELD_GROUP_INFINITY_VALUE,
    tfm_filter_allowed=True,
    input_field_group_filter_allowed=True,
    output_field_groups_filter_allowed=True,
    tfm_standard_structure=False,
)
