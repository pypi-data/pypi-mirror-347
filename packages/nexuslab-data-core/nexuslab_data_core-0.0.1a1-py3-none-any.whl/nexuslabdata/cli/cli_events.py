from nexuslabdata.logging import ErrorEvent, InfoEvent
from nexuslabdata.task import ExecutionInfo
from nexuslabdata.utils.string_utils import un_camel

####################################################################
##                      Command events                            ##
####################################################################


class CommandStarted(InfoEvent):
    def __init__(self, exec_info: ExecutionInfo):
        super().__init__()
        self.exec_info = exec_info

    def code(self) -> str:
        return "CMD-001"

    def message(self) -> str:
        return self.exec_info.get_start_message()


class CommandCompleted(InfoEvent):
    def __init__(self, exec_info: ExecutionInfo):
        super().__init__()
        self.exec_info = exec_info

    def code(self) -> str:
        return "CMD-002"

    def message(self) -> str:
        return self.exec_info.get_completion_message()


class CommandRuntimeError(ErrorEvent):
    def __init__(self, e: Exception):
        self.e = e

    def code(self) -> str:
        return "CMD-091"

    def message(self) -> str:
        return (
            f"Command runtime exception {un_camel(type(self.e).__name__)} "
            + (
                f'with message "{str(self.e.message)}".\n'
                if hasattr(self.e, "message")
                else ""
            )
        )


class ProjectLoadedSuccessfully(InfoEvent):
    def __init__(self) -> None:
        super().__init__()

    def code(self) -> str:
        return "CMD-010"

    def message(self) -> str:
        return "Project was loaded successfully"


class ConnectionFactoryLoadedSuccessfully(InfoEvent):
    def __init__(self) -> None:
        super().__init__()

    def code(self) -> str:
        return "CMD-011"

    def message(self) -> str:
        return "Connection Factory was loaded successfully"
