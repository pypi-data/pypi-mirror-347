from nexuslabdata.logging import ErrorEvent


class InvalidFlowRequestParameters(ErrorEvent):
    def __init__(
        self,
        flow_namespace: str,
        flow_name: str,
        flow_instance_name: str,
        error_message: str,
    ):
        self.flow_namespace = flow_namespace
        self.flow_name = flow_name
        self.flow_instance_name = flow_instance_name
        self.error_message = error_message

    def code(self) -> str:
        return "B-201"

    def message(self) -> str:
        return f"Invalid Flow Request Parameters for flow : {self.flow_namespace}/{self.flow_name}/{self.flow_instance_name} with message : {self.error_message}"
