from nexuslabdata.logging import DebugEvent, ErrorEvent


class ConnectionAdapterPluginImportError(ErrorEvent):
    def __init__(self, exc: str) -> None:
        self.exc = exc

    def code(self) -> str:
        return "IMP-191"

    def message(self) -> str:
        return f"{self.exc}"


class ConnectionAdapterPluginLoadError(ErrorEvent):
    def __init__(self, exc_info: str) -> None:
        self.exc_info = exc_info

    def code(self) -> str:
        return "IMP-192"

    def message(self) -> str:
        return f"{self.exc_info}"


class ConnectionAdapterPluginLoadSuccessful(DebugEvent):
    def __init__(self, type: str) -> None:
        self.type = type

    def code(self) -> str:
        return "IMP-101"

    def message(self) -> str:
        return f"Connection Adapter Plugin loaded successfully for {self.type}"
