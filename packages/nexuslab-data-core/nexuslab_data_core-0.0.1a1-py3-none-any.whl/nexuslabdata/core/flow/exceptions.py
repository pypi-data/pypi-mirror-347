from typing import Optional

from nexuslabdata.exceptions import NldRuntimeException


class InvalidFlowRequestParametersException(NldRuntimeException):
    CODE = 30001
    MESSAGE = "Invalid Flow Request Parameters Exception"

    def __init__(
        self,
        flow_namespace: str,
        flow_name: str,
        flow_instance_name: str,
        message: str,
    ) -> None:
        self.message = f"Invalid Flow Request Parameters for flow : {flow_namespace}/{flow_name}/{flow_instance_name} with message : {message}"


class FlowAdaptationFromDefinitionException(NldRuntimeException):
    CODE = 40001
    MESSAGE = "Invalid Flow Request Parameters Exception"

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message


class FlowDefinitionException(NldRuntimeException):
    CODE = 41001
    MESSAGE = "Flow Definition Standard Exception"

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message


class FlowException(NldRuntimeException):
    CODE = 42001
    MESSAGE = "Flow Standard Exception"

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message


class NoTransformationLinkFoundException(NldRuntimeException):
    CODE = 42002
    MESSAGE = "No Transformation Link Found Exception"

    def __init__(
        self,
        flow_name: str,
        src_tfm: Optional[str] = None,
        src_fld_grp: Optional[str] = None,
        tgt_tfm: Optional[str] = None,
        tgt_fld_grp: Optional[str] = None,
    ) -> None:
        self.flow_name = flow_name
        self.src_tfm = src_tfm
        self.src_fld_grp = src_fld_grp
        self.tgt_tfm = tgt_tfm
        self.tgt_fld_grp = tgt_fld_grp
        self.message = (
            f"No transformation link found in flow {flow_name} for source"
            f" {src_tfm or '#'} / {src_fld_grp or '#'}"
            f" and target {tgt_tfm or '#'} / {tgt_fld_grp or '#'}"
        )
