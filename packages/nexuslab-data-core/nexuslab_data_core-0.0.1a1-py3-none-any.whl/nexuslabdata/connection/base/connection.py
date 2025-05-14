import abc
from typing import Any, Generic, Optional, Self, TypeVar

from nexuslabdata.connection.base.credential import CREDENTIAL_TYPE
from nexuslabdata.exceptions import NotImplementedMethodException
from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.mixin import NldMixIn


class ConnectionState(NldStrEnum):
    INIT = "init"
    OPEN = "open"
    CLOSED = "closed"
    FAIL = "fail"


CONNECTION_TYPE = TypeVar("CONNECTION_TYPE")


class ConnectionWrapper(NldMixIn, Generic[CREDENTIAL_TYPE, CONNECTION_TYPE]):
    def __init__(
        self,
        name: str,
        credentials: CREDENTIAL_TYPE,
        state: ConnectionState = ConnectionState.INIT,
        connection: Optional[CONNECTION_TYPE] = None,
        session_id: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.credentials = credentials
        self.state = state
        self.connection = connection
        self.session_id = session_id

    def __post_init__(self) -> None:
        self._init_logger()

    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedMethodException(self.__class__, "type")

    # Open/Close connection methods
    @abc.abstractmethod
    def open(self) -> Self:
        """
        Opens the connection based on the available credentials.
        If the connection was successfully opened, the opened connection is loaded into the connection attribute
        and the state of connection wrapper is set to OPEN

        Returns
        -------
            The connection wrapper
        """
        raise NotImplementedMethodException(self.__class__, "open")

    def close(self) -> Self:
        """
        Closes the connection

        Returns
        -------
            This connection wrapper
        """
        if self.state in {ConnectionState.CLOSED, ConnectionState.INIT}:
            return self

        connection_closed = self._close_connection()
        if connection_closed:
            self.state = ConnectionState.CLOSED
            self.logger.info(
                f"{self.type} connection {self.name} was closed successfully"
            )

        return self

    def _close_connection(self) -> bool:
        """
        Close the connection

        Returns
        -------
            True if the connection was closed. False, otherwise.
        """
        """Perform the actual close operation."""
        if self.connection is not None:
            if hasattr(self.connection, "close"):
                self.connection.close()
                return True
        return False

    # Connection status methods
    def is_opened(self) -> bool:
        """
        Checks if the connection is currently opened

        Returns
        -------
            True if the connection is opened
        """
        return self.state == ConnectionState.OPEN

    def is_closed(self) -> bool:
        """
        Checks if the connection is currently closed

        Returns
        -------
            True if the connection is closed
        """
        return self.state == ConnectionState.CLOSED


CONNECTION = TypeVar("CONNECTION", bound=ConnectionWrapper[Any, Any])
