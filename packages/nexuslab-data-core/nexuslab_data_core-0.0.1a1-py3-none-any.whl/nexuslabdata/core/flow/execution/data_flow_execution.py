import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn


@dataclass
class DataFlowExecutionRunParam(NldNamedDataClassMixIn):
    INDEPENDENT: bool = dataclasses.field(default=False, init=False)
    content: Union[Dict[str, Any], List[Dict[str, Any]]]
    type: Optional[str] = None


@dataclass
class DataFlowExecution(NldNamedDataClassMixIn):
    task_class: str
    db_services: Optional[Dict[str, str]]
    init_params: Optional[Dict[str, Any]]
    run_params: List[DataFlowExecutionRunParam]

    def get_db_service_keys(self) -> List[str]:
        return (
            list(self.db_services.keys())
            if self.db_services is not None
            else []
        )

    def get_db_service_connection_names(self) -> List[str]:
        return (
            list(set(self.db_services.values()))
            if self.db_services is not None
            else []
        )
