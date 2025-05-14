from typing import Literal

from nexuslabdata.utils import NldStrEnum


class FlowUpdateStrategies(NldStrEnum):
    INSERT = "INSERT"
    UPSERT = "UPSERT"
    DEL_INS = "DELETE_INSERT"
    DELETE = "DELETE"


FLOW_UPDATE_STRATEGY_LITERAL = Literal[
    "INSERT", "UPSERT", "DELETE_INSERT", "DELETE"
]
