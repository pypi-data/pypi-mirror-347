import abc
from enum import Flag
from typing import Any, Tuple, Union

from nexuslabdata.utils.mixin import NldMixIn


class StepStatus(Flag):
    SUCCESS = True
    FAIL = False


class BaseStep(NldMixIn, metaclass=abc.ABCMeta):
    def __init__(self, flow_exec_uuid: str) -> None:
        super().__init__()
        self.flow_exec_uuid = flow_exec_uuid
        self._init_logger()

    @abc.abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Union[bool, Tuple[bool, Any]]:
        raise Exception(
            f"The run method is not implemented for class : {str(type(self))}"
        )

    # noinspection PyMethodMayBeStatic
    def interpret_results(self, results: Any) -> Any:
        return True
