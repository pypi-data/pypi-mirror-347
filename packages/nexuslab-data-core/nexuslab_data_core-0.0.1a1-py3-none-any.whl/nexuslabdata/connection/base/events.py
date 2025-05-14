from nexuslabdata.logging import InfoEvent

####################################################################
##                     Connection events                          ##
####################################################################


class ConnectionOpened(InfoEvent):
    def __init__(self, connection_name: str) -> None:
        self.connection_name = connection_name

    def code(self) -> str:
        return "C-101"

    def message(self) -> str:
        return f"Connection {self.connection_name} was opened"


class ConnectionClosed(InfoEvent):
    def __init__(self, connection_name: str) -> None:
        self.connection_name = connection_name

    def code(self) -> str:
        return "C-102"

    def message(self) -> str:
        return f"Connection {self.connection_name} was closed successfully"
