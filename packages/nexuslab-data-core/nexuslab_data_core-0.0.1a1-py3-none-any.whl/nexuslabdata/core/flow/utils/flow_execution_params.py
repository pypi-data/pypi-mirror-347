import datetime
from dataclasses import dataclass
from typing import Optional

from nexuslabdata.utils import NldStrEnum


class FlowExecStatus(NldStrEnum):
    SUCCEEDED = "SUCCEEDED"
    SUCCEEDED_WITH_WARNING = "SUCCEEDED WITH WARNING"
    ON_GOING = "ONGOING"
    FAILED = "FAILED"


class FlowStepExecStatus(NldStrEnum):
    SUCCEEDED = "SUCCEEDED"
    SUCCEEDED_WITH_WARNING = "WARNING"
    FAILED = "FAILED"


@dataclass
class FlowStepExecutionInfo:
    flow_exec_uuid: str
    step_name: str
    started_at: datetime.datetime
    ended_at: datetime.datetime
    data_load_strategy: str
    requestor: str
    query: Optional[str] = None
    step_exec_status: Optional[str] = None
    step_error: Optional[str] = None
    source_rows_in_success: int = 0
    source_rows_in_error: int = 0
    target_rows_inserted_in_success: int = 0
    target_rows_inserted_in_error: int = 0
    target_rows_updated_in_success: int = 0
    target_rows_updated_in_error: int = 0
    target_rows_deleted_in_success: int = 0
    target_rows_deleted_in_error: int = 0
