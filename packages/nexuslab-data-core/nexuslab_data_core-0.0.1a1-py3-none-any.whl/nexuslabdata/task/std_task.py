import abc
from typing import Any, List

from nexuslabdata.cli import cli_variables
from nexuslabdata.task.base_task import BaseTask
from nexuslabdata.task.execution import ExecutionInfo


class StandardTask(BaseTask, metaclass=abc.ABCMeta):
    """
    Standard Client Task
    """

    init_params: List[str] = [cli_variables.EXC_INFO]
    run_params: List[str] = []

    def __init__(self, exc_info: ExecutionInfo, **kwargs: Any) -> None:
        self.exc_info = exc_info

        super().__init__(
            exec_uuid=self.exc_info.uuid if self.exc_info is not None else None
        )
