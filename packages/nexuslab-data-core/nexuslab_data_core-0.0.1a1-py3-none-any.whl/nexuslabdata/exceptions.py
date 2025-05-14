import builtins
from typing import Any, Dict


class NldException(builtins.Exception):
    CODE = -999999
    MESSAGE = "Server Error"

    def data(self) -> Dict[str, str]:
        # if overriden, make sure the result is json-serializable.
        return {
            "type": self.__class__.__name__,
            "message": str(self),
        }


class NldRuntimeException(RuntimeError, NldException):
    CODE = 10001
    MESSAGE = "Runtime error"

    def __init__(self, msg: str) -> None:
        self.message = msg

    ####################################################################
    ##                     Generic exceptions                         ##
    ####################################################################

    ####################################################################
    ##                     Argument exceptions                        ##
    ####################################################################


class ArgumentException(NldRuntimeException):
    CODE = 10001
    MESSAGE = "Argument Exception"


class MissingMandatoryArgumentException(ArgumentException):
    CODE = 10002
    MESSAGE = "Missing Mandatory Argument Exception"

    def __init__(
        self, object_type: type, method_name: str, argument_name: str
    ) -> None:
        self.message = f"Missing mandatory argument '{argument_name}' on call of method {method_name} on {object_type.__name__}"


class InvalidTypeArgumentException(ArgumentException):
    CODE = 10003
    MESSAGE = "Invalid Type Argument Exception"

    def __init__(
        self,
        object_type: type,
        method_name: str,
        argument_name: str,
        arg_expected_type: type,
        arg_type: type,
    ) -> None:
        self.message = (
            f"Invalid type for argument '{argument_name}' on call of method {method_name} on {object_type.__name__}. "
            + f"The expected type of the argument is {str(arg_expected_type)} but the argument type was {str(arg_type)}"
        )

    ####################################################################
    ##                 Implementation exceptions                      ##
    ####################################################################


class ImplementationException(NldRuntimeException):
    CODE = 10101
    MESSAGE = "Implementation Exception"


class NotImplementedMethodException(NldRuntimeException):
    CODE = 10102
    MESSAGE = "Method Missing Implementation Exception"

    def __init__(self, obj_class: type, method_name: str) -> None:
        self.message = f"The {method_name} method is not implemented for class : {str(type(obj_class))}"

    ####################################################################
    ##                       File exceptions                          ##
    ####################################################################


class NoFileAtLocationException(NldRuntimeException):
    CODE = 11001
    MESSAGE = "No file available at location"

    def __init__(self, file_path: str) -> None:
        self.message = "No file available at location : " + file_path


class ConfigurationFolderNotValid(NldRuntimeException):
    CODE = 11011
    MESSAGE = "Configuration Folder is not valid"

    def __init__(self, file_path: str) -> None:
        self.message = (
            "The configuration folder provided is not valid : " + file_path
        )

    ####################################################################
    ##                    Data Class exceptions                       ##
    ####################################################################


class DataClassReadException(NldRuntimeException):
    CODE = 21001
    MESSAGE = "Issue during the read for a data class"

    def __init__(self, data_class_name: str, method_name: str) -> None:
        self.message = f"The read ({method_name}) failed for data class : {data_class_name}. Please check the log for more details."


class DataClassDeepCopyException(NldRuntimeException):
    CODE = 21001
    MESSAGE = "Issue during the data class deep copy"

    def __init__(self, self_object: Any, expected_class: Any) -> None:
        object_display_name = (
            self_object.__str__ if self_object is not None else "None"
        )
        self.message = (
            f"The deep copy failed for data class : {expected_class.__name__} on object {object_display_name}. "
            f"Please check the log for more details."
        )

    ####################################################################
    ##                    Connection exceptions                       ##
    ####################################################################


class ConnectionCouldNotBeOpenedException(NldRuntimeException):
    CODE = 31001
    MESSAGE = "Connection could not be opened"

    def __init__(self, connection_name: str) -> None:
        self.message = f"The connection {connection_name} could not be opened. Please check the log for more details."

    ####################################################################
    ##                  In-memory object exceptions                   ##
    ####################################################################


class MissingObjectException(NldRuntimeException):
    CODE = 41001
    MESSAGE = "Object could not be found based on name"

    def __init__(self, object_type: type, object_name: str) -> None:
        self.message = (
            f"Missing object {object_type.__name__} with name : {object_name}"
        )


class NoObjectLoadedException(NldRuntimeException):
    CODE = 41002
    MESSAGE = "No object loaded from file"

    def __init__(self, object_type: type, file_path: str) -> None:
        self.message = (
            f"No object {object_type.__name__} was loaded from file {file_path}"
        )
