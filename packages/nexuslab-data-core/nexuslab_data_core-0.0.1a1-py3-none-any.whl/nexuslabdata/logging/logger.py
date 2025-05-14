import logging
from typing import Optional, cast

from nexuslabdata.logging.base import (
    BaseEvent,
    EventLevel,
    StandardDebugEvent,
    StandardErrorEvent,
    StandardInfoEvent,
)


class NldLogger(logging.Logger):
    """
    This logger should be set as the logger class for the package
    logging, by using the following line of code in the main method
        - logging.setLoggerClass(NldLogger)
    """

    def __init__(self, name: str, level: int = 0) -> None:
        super().__init__(name, level)

    def log_event(self, event: BaseEvent) -> None:
        self.log(event.level(), event.message())


def log_event_default(event: BaseEvent) -> None:
    lcl_logger: NldLogger = cast(NldLogger, logging.getLogger("ndl"))
    lcl_logger.log_event(event)


def log_info_default(message: str) -> None:
    lcl_logger: NldLogger = cast(NldLogger, logging.getLogger("ndl"))
    lcl_logger.log_event(StandardInfoEvent(msg=message))


def log_debug_default(message: str) -> None:
    lcl_logger: NldLogger = cast(NldLogger, logging.getLogger("ndl"))
    lcl_logger.log_event(event=StandardDebugEvent(msg=message))


def log_error_default(message: str) -> None:
    lcl_logger: NldLogger = cast(NldLogger, logging.getLogger("ndl"))
    lcl_logger.log_event(StandardErrorEvent(msg=message))


def log_event(event: BaseEvent, logger: Optional[NldLogger] = None) -> None:
    if logger is not None and isinstance(type(logger), NldLogger):
        logger.log_event(event)
    else:
        log_event_default(event)


class NldLoggable:
    """Interface for all the loggable classes.

    Initializes the local logger and provides standard logging methods.
    """

    def __init__(self) -> None:
        self._init_logger()

    def _init_logger(self) -> None:
        self.logger: NldLogger = cast(
            NldLogger, logging.getLogger(self.__class__.__name__)
        )

    def log_event(self, event: BaseEvent) -> None:
        """Logs the provided event

        Attributes
        ----------
        event : BaseEvent
            The event to log, containing the level and message
        """
        log_event(event, self.logger)


class LoggerManager:
    """
    This logger manager initializes the default logging with the custom DF classes and levels
    """

    def __init__(
        self,
        level: int = logging.DEBUG,
        format: str = "[%(asctime)s] [%(levelname)s] - %(message)s",
    ) -> None:
        logging.setLoggerClass(NldLogger)
        logging.basicConfig(level=level, format=format)
        logging.addLevelName(EventLevel.TEST, "TEST")


def init_logger_for_tests() -> None:
    LoggerManager(EventLevel.TEST)
