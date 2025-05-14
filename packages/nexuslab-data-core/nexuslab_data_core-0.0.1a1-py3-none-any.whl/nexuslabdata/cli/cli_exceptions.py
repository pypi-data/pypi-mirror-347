from click.exceptions import ClickException


class ExceptionExit(ClickException):
    """This class wraps any exception that does not contain results thrown while invoking nld commands."""

    def __init__(self, exception: Exception) -> None:
        super().__init__(exception.__str__())
        self.exception = exception
