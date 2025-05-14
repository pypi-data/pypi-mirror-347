import csv
import datetime
import os
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import jinja2
import pandas as pd

from nexuslabdata.connection.base.exceptions import QueryExecutionException
from nexuslabdata.core import Structure
from nexuslabdata.logging import log_event
from nexuslabdata.logging.events import CSVFileWriteSuccessful
from nexuslabdata.utils.mixin import NldMixIn


@dataclass
class QueryWrapper(NldMixIn):
    query: str
    interpreted_query: Optional[str] = None
    name: str = ""
    params: Dict[str, Union[str, Dict[str, Any]]] = field(default_factory=dict)
    runtime_exception_message: Optional[str] = None

    def update_interpreted_query(self) -> None:
        self.interpreted_query = jinja2.Template(self.query).render(
            **self.params
        )

    def get_interpreted_query(self) -> str:
        if self.interpreted_query is None:
            self.update_interpreted_query()
        return cast(str, self.interpreted_query)

    def raise_runtime_exception(self) -> None:
        if self.runtime_exception_message is not None:
            raise QueryExecutionException(
                error_message=self.runtime_exception_message.format(
                    **self.params
                )
            )


class QueryExecResultStatus(StrEnum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclass
class QueryExecResult(NldMixIn):
    """
    Query Execution Result Wrapper

    All the queries returned by the method execute_query should return this object
    """

    query_name: str
    exec_status: str
    query: str
    query_id: Optional[str]
    result_set: Optional[list[Any]]
    result_set_structure: Optional[Structure]
    start_tst: datetime.datetime
    end_tst: datetime.datetime

    # Status methods

    def succeeded(self) -> bool:
        return self.exec_status == QueryExecResultStatus.SUCCESS

    def failed(self) -> bool:
        return self.exec_status == QueryExecResultStatus.ERROR

    def get_error_message(self) -> str:
        if self.failed():
            if self.result_set is not None:
                error_message = self.result_set[0]
                if error_message is not None:
                    if type(error_message) is str:
                        return (
                            error_message.replace("\n", " ")
                            .replace("\r", " ")
                            .strip()
                        )
        return ""

    @property
    def query_type(self) -> str:
        return self.query.strip().split()[0].upper()

    # Dictionary methods

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_name": self.query_name,
            "exec_status": self.exec_status,
            "query": self.query,
            "query_id": self.query_id,
            "result_set": self.result_set,
            "result_set_header": ", ".join(
                [field.name for field in self.result_set_structure.fields]
            )
            if self.result_set_structure is not None
            else "",
            "start_tst": self.start_tst.strftime("%Y%m%d%H%M%S%f"),
            "end_tst": self.end_tst.strftime("%Y%m%d%H%M%S%f"),
        }

    # Pandas methods
    def get_result_set_as_df(self) -> pd.DataFrame:
        if self.result_set_structure is not None:
            return pd.DataFrame(
                self.result_set,
                columns=[
                    field.name for field in self.result_set_structure.fields
                ],
            )
        else:
            return pd.DataFrame()

    def get_result_set_as_dict(self) -> Any:
        if self.succeeded():
            result_set_df = self.get_result_set_as_df()
            if result_set_df.shape[0] == 0:
                self.log_error(f"Query {self.query_name} retrieved O rows.")
            else:
                if result_set_df.shape[0] > 1:
                    self.log_error(
                        f"Query {self.query_name} contains more than 1 rows. "
                        f"The method to get dictionary result is meant "
                        f"for single rows result set"
                    )
                else:
                    return result_set_df.iloc[0].to_dict()
        else:
            self.log_error(f"Query {self.query_name} encountered an error.")

        return {}

    def get_result_set_as_single_value(self) -> Any:
        result_set_df = self.get_result_set_as_df()
        if result_set_df.shape[0] == 0:
            self.log_error(f"Query {self.query_name} retrieved O rows.")
        else:
            if result_set_df.shape[1] == 1:
                return result_set_df.iloc[0, 0]
            else:
                self.log_error(
                    f"Query {self.query_name} contains more than 1 column. The "
                    f"first column"
                    f"data is used for returning the single value."
                )


class QueryExecResults(List[QueryExecResult]):
    def __init__(self) -> None:
        super().__init__()

    def get_status(self) -> str:
        if self.has_succeeded():
            return QueryExecResultStatus.SUCCESS
        return QueryExecResultStatus.ERROR

    def has_succeeded(self) -> bool:
        for query_exec_result in self:
            if query_exec_result.failed():
                return False
        return True

    def has_failed(self) -> bool:
        for query_exec_result in self:
            if query_exec_result.failed():
                return True
        return False

    def get_number_of_results(self) -> int:
        return len(self)

    def to_str(self) -> str:
        return ", ".join(
            [str(query_exec_result.to_dict()) for query_exec_result in self]
        )

    def report_exec_status(self) -> str:
        return "\n".join(
            [
                (
                    query_exec_result.query_name
                    if query_exec_result.query_name is not None
                    else ""
                )
                + " : "
                + query_exec_result.exec_status
                + (
                    "(" + query_exec_result.get_error_message() + ")"
                    if query_exec_result.failed()
                    else ""
                )
                for query_exec_result in self
            ]
        )

    def get_csv_header(self) -> List[str]:
        return [
            "Query Name",
            "Query",
            "Execution Status",
            "Execution Message",
            "Start Tst",
            "End Tst",
        ]

    def get_csv_rows(self) -> List[list[Any]]:
        return [
            [
                query_exec_result.query_name,
                query_exec_result.query[
                    0 : 100
                    if len(query_exec_result.query) >= 100
                    else len(query_exec_result.query)
                ]
                .replace("\n", " ")
                .replace("\r", " ")
                .replace(";", " "),
                query_exec_result.exec_status,
                query_exec_result.get_error_message(),
                query_exec_result.start_tst.strftime("%Y-%m-%d %H:%M:%S.%f"),
                query_exec_result.end_tst.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ]
            for query_exec_result in self
        ]

    def to_csv(
        self,
        file_path: str,
        delimiter: str = ";",
        newline: str = "\n",
        quotechar: str = '"',
    ) -> None:
        with open(file_path, "w", newline=newline) as csvfile:
            writer = csv.writer(
                csvfile, delimiter=delimiter, quotechar=quotechar
            )
            writer.writerow(self.get_csv_header())
            for query_exec_result_csv_row in self.get_csv_rows():
                writer.writerow(query_exec_result_csv_row)
        log_event(
            CSVFileWriteSuccessful(
                file_path=file_path, object_type_name=QueryExecResults.__name__
            ),
        )


class QueryExecResultUtil:
    @classmethod
    def write_script_exec_results_to_csv(
        cls,
        script_results: List[Tuple[str, QueryExecResults]],
        file_path: str,
        delimiter: str = ";",
        newline: str = "\n",
        quotechar: str = '"',
    ) -> None:
        with open(file_path, "w", newline=newline) as csvfile:
            writer = csv.writer(
                csvfile, delimiter=delimiter, quotechar=quotechar
            )
            writer.writerow(
                [
                    "Script Name",
                    "Script Status",
                    "Query Name",
                    "Query",
                    "Query Status",
                    "Execution Message",
                    "Start Tst",
                    "End Tst",
                ]
            )
            for script_result in script_results:
                script_name = os.path.basename(script_result[0])
                query_exec_result = script_result[1]
                for (
                    query_exec_result_csv_row
                ) in query_exec_result.get_csv_rows():
                    csv_row = [script_name, query_exec_result.get_status()]
                    csv_row.extend(query_exec_result_csv_row)
                    writer.writerow(csv_row)
        log_event(
            CSVFileWriteSuccessful(
                file_path=file_path, object_type_name="ScriptExecResults"
            ),
        )
