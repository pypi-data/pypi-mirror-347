from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import nexuslabdata.utils.datetime_util as datetime_util
from nexuslabdata.utils import NldStrEnum


class ExecutionStatus(NldStrEnum):
    ONGOING = "ONGOING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


@dataclass
class ExecutionInfo:
    command: str
    uuid: str
    started_at: datetime
    success: Optional[bool]
    completed_at: Optional[datetime]

    def get_execution_status(self) -> str:
        return (
            ExecutionStatus.SUCCEEDED
            if self.success
            else ExecutionStatus.FAILED
        )

    def get_start_message(self) -> str:
        started_at_str = datetime_util.format_timestamp_to_hour_string(
            self.started_at
        )
        return f"Command `{self.command}` started at {started_at_str} with uuid {self.uuid}"

    def get_completion_message(self) -> str:
        status = (
            ExecutionStatus.SUCCEEDED.lower()
            if self.success
            else ExecutionStatus.FAILED.lower()
        )
        elapsed = (
            self.completed_at - self.started_at
            if self.completed_at is not None
            else timedelta()
        )
        started_at_str = datetime_util.format_timestamp_to_hour_string(
            self.started_at
        )
        completed_at_str = datetime_util.format_timestamp_to_hour_string(
            self.completed_at
            if self.completed_at is not None
            else datetime_util.get_current_datetime()
        )
        return (
            f"Command `{self.command}` {status} at {completed_at_str}  with a duration of {datetime_util.format_to_human_readable_duration(elapsed)} ("
            f"started at {started_at_str})"
        )
