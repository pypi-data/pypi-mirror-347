import dataclasses
from typing import Optional

from nexuslabdata.core.flow.incremental import FLOW_INCREMENTAL_TYPE_LITERAL
from nexuslabdata.core.flow.utils import FLOW_LOADING_STRATEGY_LITERAL
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclasses.dataclass
class FlowConfig(NldDataClassMixIn):
    flow_namespace: str
    flow_name: str
    flow_instance_name: str
    target_schema: str
    target_table: str
    default_data_loading_strategy: FLOW_LOADING_STRATEGY_LITERAL
    historical_refresh_authorized: bool
    incremental_type: FLOW_INCREMENTAL_TYPE_LITERAL
    pull_field_name: Optional[str] = None
    pull_field_format: Optional[str] = None
    target_field_name_for_previous_layer_last_update_tst: Optional[str] = None
    target_field_name_for_source_extraction_tst: Optional[str] = None
    target_field_name_for_source_last_update_tst: Optional[str] = None
    delta_period_reference_type: Optional[str] = None
    delta_period_reference: Optional[str] = None
    delta_period_range_from_type: Optional[str] = None
    delta_period_range_from: Optional[str] = None
    delta_period_range_to_type: Optional[str] = None
    delta_period_range_to: Optional[str] = None
