import dataclasses
import datetime
import uuid
from typing import Literal, Optional, cast

from nexuslabdata.core.flow.exceptions import (
    InvalidFlowRequestParametersException,
)
from nexuslabdata.core.flow.utils import FlowLoadingStrategies
from nexuslabdata.utils import NldStrEnum
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn
from nexuslabdata.utils.datetime_util import (
    COMPACT_DATETIME_FORMAT,
    get_current_datetime,
)


class FlowRequestStatus(NldStrEnum):
    PLANNED = "PLANNED"
    CANCELLED = "CANCELLED"
    ONGOING = "ONGOING"


FLOW_REQUEST_STATUS_LITERAL = Literal["PLANNED", "CANCELLED", "ONGOING"]


class FlowRequestType(NldStrEnum):
    FIXED_RANGE_TST = "FIXED_RANGE_TST"
    FIXED_RANGE = "FIXED_RANGE"
    FUNCTIONAL_KEY = "FUNC_KEY"
    FULL = "FULL"


FLOW_REQUEST_TYPE_LITERAL = Literal[
    "FIXED_RANGE_TST", "FIXED_RANGE", "FUNC_KEY", "FULL"
]


@dataclasses.dataclass
class FlowRequest(NldDataClassMixIn):
    request_uid: str
    flow_namespace: str
    flow_name: str
    flow_instance_name: str
    request_type: str
    flow_loading_strategy: str
    run_status: FLOW_REQUEST_STATUS_LITERAL
    requestor_name: Optional[str] = None
    request_description: Optional[str] = None
    pull_from: Optional[datetime.datetime] = None
    pull_to: Optional[datetime.datetime] = None
    pull_filter: Optional[str] = None
    load_from: Optional[datetime.datetime] = None
    load_to: Optional[datetime.datetime] = None
    load_filter: Optional[str] = None
    functional_key: Optional[str] = None
    delta_period_range_from_type: Optional[str] = None
    delta_period_range_from: Optional[str] = None
    delta_period_range_to_type: Optional[str] = None
    delta_period_range_to: Optional[str] = None

    @classmethod
    def generate_uuid(cls) -> str:
        return uuid.uuid4().__str__()

    @classmethod
    def create_fixed_range_tst_timestamp_on_pull_request_to_plan(
        cls,
        flow_namespace: str,
        flow_name: str,
        flow_instance_name: str,
        request_description: Optional[str] = None,
        requestor_name: Optional[str] = None,
        flow_loading_strategy: Optional[str] = None,
        pull_from: Optional[datetime.datetime] = None,
        pull_to: Optional[datetime.datetime] = None,
        pull_filter: Optional[str] = None,
    ) -> "FlowRequest":
        cls.check_flow_loading_strategy_valid_for_request(flow_loading_strategy)
        flow_loading_strategy = cast(str, flow_loading_strategy)
        if flow_loading_strategy == FlowLoadingStrategies.RECOVERY_DELTA:
            if pull_from is None:
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range Timestamp - Recovery Delta - Pull from is mandatory and was not provided",
                )
            if pull_from > get_current_datetime():
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range Timestamp - Recovery Delta - Pull from should be prior to the current timestamp "
                    + "- From : "
                    + pull_from.strftime(COMPACT_DATETIME_FORMAT),
                )
        if flow_loading_strategy == FlowLoadingStrategies.RECOVERY:
            if pull_from is None:
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range Timestamp - Recovery - Pull from is mandatory and was not provided",
                )
            if pull_to is None:
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range Timestamp - Recovery - Pull to is mandatory and was not provided",
                )
            if pull_from > pull_to:
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range Timestamp - Recovery - Pull from should be prior to the pull to - From : "
                    + pull_from.strftime(COMPACT_DATETIME_FORMAT)
                    + " / To : "
                    + pull_to.strftime(COMPACT_DATETIME_FORMAT),
                )

        return FlowRequest(
            request_uid=cls.generate_uuid(),
            flow_namespace=flow_namespace,
            flow_name=flow_name,
            flow_instance_name=flow_instance_name,
            request_description=request_description,
            request_type=FlowRequestType.FIXED_RANGE_TST.value,
            requestor_name=requestor_name,
            flow_loading_strategy=flow_loading_strategy,
            run_status=FlowRequestStatus.PLANNED.value,
            pull_from=pull_from,
            pull_to=pull_to,
            pull_filter=pull_filter,
        )

    @classmethod
    def create_fixed_range_timestamp_on_pull_request_to_plan(
        cls,
        flow_namespace: str,
        flow_name: str,
        flow_instance_name: str,
        request_description: Optional[str] = None,
        requestor_name: Optional[str] = None,
        flow_loading_strategy: Optional[str] = None,
        delta_period_range_from_type: Optional[str] = None,
        delta_period_range_from: Optional[str] = None,
        delta_period_range_to_type: Optional[str] = None,
        delta_period_range_to: Optional[str] = None,
    ) -> "FlowRequest":
        cls.check_flow_loading_strategy_valid_for_request(flow_loading_strategy)
        flow_loading_strategy = cast(str, flow_loading_strategy)
        if flow_loading_strategy == FlowLoadingStrategies.RECOVERY_DELTA:
            if (
                delta_period_range_from_type is None
                or delta_period_range_from is None
            ):
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range - Recovery Delta - Period Range From Type and Value are mandatory and were not provided",
                )
        if flow_loading_strategy == FlowLoadingStrategies.RECOVERY:
            if (
                delta_period_range_from_type is None
                or delta_period_range_from is None
            ):
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range - Recovery - Period Range From Type and Value are mandatory and were not provided",
                )
            if (
                delta_period_range_to_type is None
                or delta_period_range_to is None
            ):
                raise InvalidFlowRequestParametersException(
                    flow_namespace,
                    flow_name,
                    flow_instance_name,
                    "Fixed Range - Recovery - Period Range To Type and Value are mandatory and were not provided",
                )

        return FlowRequest(
            request_uid=cls.generate_uuid(),
            flow_namespace=flow_namespace,
            flow_name=flow_name,
            flow_instance_name=flow_instance_name,
            request_description=request_description,
            request_type=FlowRequestType.FIXED_RANGE.value,
            requestor_name=requestor_name,
            flow_loading_strategy=flow_loading_strategy,
            run_status=FlowRequestStatus.PLANNED.value,
            delta_period_range_from_type=delta_period_range_from_type,
            delta_period_range_from=delta_period_range_from,
            delta_period_range_to_type=delta_period_range_to_type,
            delta_period_range_to=delta_period_range_to,
        )

    @classmethod
    def create_target_functional_key_request_to_plan(
        cls,
        flow_namespace: str,
        flow_name: str,
        flow_instance_name: str,
        request_description: Optional[str] = None,
        requestor_name: Optional[str] = None,
        flow_loading_strategy: Optional[str] = None,
        functional_key: Optional[str] = None,
    ) -> "FlowRequest":
        cls.check_flow_loading_strategy_valid_for_request(flow_loading_strategy)
        flow_loading_strategy = cast(str, flow_loading_strategy)
        if functional_key is None:
            raise InvalidFlowRequestParametersException(
                flow_namespace,
                flow_name,
                flow_instance_name,
                "Functional Key - Recovery Delta - Functional Key information is mandatory and was not provided",
            )

        return FlowRequest(
            request_uid=cls.generate_uuid(),
            flow_namespace=flow_namespace,
            flow_name=flow_name,
            flow_instance_name=flow_instance_name,
            request_description=request_description,
            request_type=FlowRequestType.FUNCTIONAL_KEY.value,
            requestor_name=requestor_name,
            flow_loading_strategy=flow_loading_strategy,
            run_status=FlowRequestStatus.PLANNED.value,
            functional_key=functional_key,
        )

    @classmethod
    def check_flow_loading_strategy_valid_for_request(
        cls, flow_loading_strategy: Optional[str]
    ) -> None:
        if flow_loading_strategy is None:
            raise ValueError(
                "Flow Loading Strategy requires a loading strategy"
            )
        if flow_loading_strategy not in [
            FlowLoadingStrategies.RECOVERY.value,
            FlowLoadingStrategies.RECOVERY_DELTA.value,
        ]:
            raise ValueError(
                "Flow Loading Strategy for a request is expected to be one of the values : "
                + ",".join(
                    [
                        FlowLoadingStrategies.RECOVERY.value,
                        FlowLoadingStrategies.RECOVERY_DELTA.value,
                    ]
                )
            )
