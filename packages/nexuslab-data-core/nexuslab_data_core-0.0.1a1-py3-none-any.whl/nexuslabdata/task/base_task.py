import abc
import uuid
from enum import Flag
from typing import Any, Dict, List, Optional

from nexuslabdata.exceptions import MissingMandatoryArgumentException
from nexuslabdata.utils.mixin import NldMixIn


class BaseRunStatus(Flag):
    SUCCESS = True
    FAIL = False


class BaseTask(NldMixIn, metaclass=abc.ABCMeta):
    init_params: List[str] = []
    run_params: List[str] = []

    def __init__(self, exec_uuid: Optional[str] = None) -> None:
        super().__init__()
        self._init_logger()
        self.exec_uuid = (
            uuid.uuid4().__str__() if exec_uuid is None else exec_uuid
        )

    @classmethod
    def check_init_params_dict(cls, params_dict: Dict[str, Any]) -> None:
        for init_param in cls.init_params:
            if init_param not in list(params_dict.keys()):
                raise MissingMandatoryArgumentException(
                    cls, "__init__", init_param
                )

    @classmethod
    def check_run_params_dict(cls, params_dict: Dict[str, Any]) -> None:
        for run_param in cls.run_params:
            if run_param not in list(params_dict.keys()):
                raise MissingMandatoryArgumentException(cls, "run", run_param)

    @abc.abstractmethod
    def run(self, **kwargs: Any) -> Any:
        raise Exception(
            f"The run method is not implemented for class : {str(type(self))}"
        )

    # noinspection PyMethodMayBeStatic
    def interpret_results(self, results: Any) -> Any:
        return True
