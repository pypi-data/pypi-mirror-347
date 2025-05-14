import logging

from nexuslabdata.core.flow import DataFlowExecution
from nexuslabdata.service.object_std_service import (
    ObjectDefinition,
    ObjectStandardProviderService,
)
from nexuslabdata.utils import NldStrEnum

logger = logging.getLogger(__name__)


class DataFlowObjectNames(NldStrEnum):
    DATA_FLOW_EXECUTION = "data_flow_execution"


class DataFlowObjects:
    DATA_FLOW_EXECUTION = ObjectDefinition(
        name=DataFlowObjectNames.DATA_FLOW_EXECUTION.value,
        data_class=DataFlowExecution,
        folder_name="data_flow_execution",
    )


DATA_FLOW_OBJECTS = [
    DataFlowObjects.DATA_FLOW_EXECUTION,
]


class DataFlowService(ObjectStandardProviderService):
    def __init__(self) -> None:
        super().__init__(object_definitions=DATA_FLOW_OBJECTS)
