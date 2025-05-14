from nexuslabdata.exceptions import NldRuntimeException


class QueryExecutionException(NldRuntimeException):
    CODE = 30011
    MESSAGE = "Query Execution Exception"

    def __init__(self, error_message: str) -> None:
        self.message = f"{error_message}"


class NoDbServiceAvailableException(NldRuntimeException):
    CODE = 30001
    MESSAGE = "No DB Service available exception"

    def __init__(self, connection_name: str) -> None:
        self.message = (
            f"No db service is available for name : '{connection_name}'"
        )


class DbServiceAlreadyAvailableException(NldRuntimeException):
    CODE = 30002
    MESSAGE = "DB Service is already available exception"

    def __init__(self, connection_name: str) -> None:
        self.message = f"The db service is already available for for name : '{connection_name}'"


class RequestOnClosedConnectionException(NldRuntimeException):
    CODE = 30101
    MESSAGE = "Request on closed connection Exception"

    def __init__(self, connection_name: str, request_desc: str) -> None:
        self.message = (
            f"A request '{request_desc}' was done on the non-opened connection {connection_name}. Ensure "
            f"connection is opened."
        )


class UnavailableConnectionException(NldRuntimeException):
    CODE = 30201
    MESSAGE = "Unavailable connection exception"

    def __init__(self, connection_name: str) -> None:
        self.message = f"Connection {connection_name} is not available"


class UnavailableConnectionProfileException(NldRuntimeException):
    CODE = 30202
    MESSAGE = "Unavailable connection profile exception"

    def __init__(self, connection_name: str, profile_name: str) -> None:
        self.message = f"No profile {profile_name} on connection {connection_name} is not available"
