from typing import Literal

from nexuslabdata.utils import NldStrEnum


class FlowLoadingStrategies(NldStrEnum):
    FULL = "FULL"
    DELTA = "DLT"
    UNIT = "UNIT"
    RECOVERY_DELTA = "REC-DLT"
    RECOVERY = "REC"


FLOW_LOADING_STRATEGY_LITERAL = Literal["FULL", "DLT", "UNIT", "REC-DLT", "REC"]
