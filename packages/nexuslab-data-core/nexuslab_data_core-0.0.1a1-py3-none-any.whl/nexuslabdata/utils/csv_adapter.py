import csv
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

from nexuslabdata.logging import log_event
from nexuslabdata.logging.events import CSVFileWriteSuccessful
from nexuslabdata.utils.data_class_flatten_adapter import (
    DEFAULT_SEPARATOR_INSIDE_FIELDS_EQUAL,
    DEFAULT_SEPARATOR_INSIDE_FIELDS_SECOND_LEVEL,
    ListFlattenAdapter,
)
from nexuslabdata.utils.mixin import NldMixIn

C = TypeVar("C", bound=Any)


class CsvRowDefinition:
    def __init__(self, name: str, method_rule: str):
        self.name = name
        self.method_rule = method_rule


class CsvDataSchema:
    def __init__(
        self,
        row_type_column_position: int,
        row_types: List[CsvRowDefinition],
        header_row_list: List[str],
        adapter: Type[ListFlattenAdapter[C]],
    ):
        if row_types is None:
            raise ValueError("Csv Data Schema requires a list of row types")
        if len(row_types) == 0:
            raise ValueError("Csv Data Schema requires a list of row types")
        self.row_type_column_position = row_type_column_position
        self.row_types = row_types
        self.header_row_list = header_row_list
        self.adapter = adapter

    def get_first_element(self) -> str:
        return self.row_types[0].name

    def get_row_type_names(self) -> List[str]:
        return [row_type.name for row_type in self.row_types]

    def get_row_type_as_dict(self) -> Dict[str, CsvRowDefinition]:
        return {row_type.name: row_type for row_type in self.row_types}

    def get_row_type_by_name(self, name: str) -> CsvRowDefinition:
        return self.get_row_type_as_dict()[name]


class CsvAdapter(NldMixIn, Generic[C]):
    """
    Standard Class to read/write csv files
    """

    def __init__(self, csv_data_schema: CsvDataSchema):
        super().__init__()
        self.csv_data_schema = csv_data_schema

    def read_csv(
        self,
        content: Iterable[str],
        delimiter: str = ";",
        quotechar: str = '"',
    ) -> List[C]:
        object_list: List[C] = []
        for object_dict in self.read_csv_content_to_list(
            content=content,
            delimiter=delimiter,
            quotechar=quotechar,
        ):
            object_list.append(self._create_object_from_rows(object_dict))
        return object_list

    def read_csv_from_file(
        self,
        file_path: str,
        newline: str = "",
        delimiter: str = ";",
        quotechar: str = '"',
        encoding: str = "ISO 8859-1",
    ) -> List[C]:
        """
        Reads csv format with the standard description of structures and returns a list of the class

        Parameters
        -----------
            file_path : the csv data dictionary file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)
            encoding : the encoding of the file to read

        Returns
        -----------
            A list of objects based on the data available in the csv file
        """
        with open(file_path, newline=newline, encoding=encoding) as csvfile:
            next(csvfile)
            objects_read = self.read_csv(csvfile, delimiter, quotechar)
        # TODO Check why logger fails on this event
        """
        self.log_event(
            CSVFileReadSuccessful(object_type_name="", file_path=file_path)
        )
        """
        return objects_read

    def read_csv_content_to_list(
        self, content: Iterable[str], delimiter: str = ";", quotechar: str = '"'
    ) -> List[Dict[str, List[Any]]]:
        """
        Reads csv format with the standard description of structures and returns a list of the class

        Parameters
        -----------
            content : the content
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)

        Returns
        -----------
            A list of objects based on the data available in the csv file
        """
        objects_read: List[Dict[str, List[Any]]] = []
        current_object: Dict[str, List[Any]] = {}

        reader = csv.reader(content, delimiter=delimiter, quotechar=quotechar)
        i = 0
        for row in reader:
            row_type = row[self.csv_data_schema.row_type_column_position]
            if str(row_type) == self.csv_data_schema.get_first_element():
                if i != 0:
                    objects_read.append(current_object)
                current_object = {}

            row_type_info = self.csv_data_schema.get_row_type_by_name(row_type)
            current_row_type_name = row_type_info.name
            new_object = eval(row_type_info.method_rule)
            if current_row_type_name in current_object.keys():
                current_list: List[Dict[str, List[Any]]] = current_object[
                    current_row_type_name
                ]
                current_list.append(new_object)
            else:
                current_object.update({current_row_type_name: [new_object]})
            i += 1

        # After the read, add the last found structure to the structures read
        objects_read.append(current_object)
        return objects_read

    def _create_object_from_rows(self, object_dict: Dict[str, List[Any]]) -> C:
        raise NotImplementedError(
            "The _create_object_from_rows method is not implemented"
        )

    def format_object_to_array(
        self, obj: List[C]
    ) -> List[Tuple[Optional[int | str], ...]]:
        output_list: List[Tuple[Optional[int | str], ...]] = []
        for structure in obj:
            output_list.extend(self.csv_data_schema.adapter.flatten(structure))
        return self.clean_object_arrays(obj_arrays=output_list)

    def get_max_data_columns(self) -> int:
        return len(self.csv_data_schema.header_row_list)

    def clean_object_arrays(
        self, obj_arrays: List[Tuple[Optional[int | str], ...]]
    ) -> List[Tuple[Optional[int | str], ...]]:
        # Ensure all the items in the output list contains the maximum expected of data columns.
        # If that's not the case, extend the list
        for output_entry in obj_arrays:
            self.clean_object_array(output_entry)
        return obj_arrays

    def clean_object_array(
        self, obj_array: Tuple[Optional[int | str], ...]
    ) -> Tuple[Optional[int | str], ...]:
        # Ensure all the items in the output list contains the maximum expected of data columns.
        # If that's not the case, extend the list
        if len(obj_array) < self.get_max_data_columns():
            obj_array = obj_array + tuple(
                [None] * (self.get_max_data_columns() - len(obj_array))
            )
        return obj_array

    def to_csv(
        self,
        file_path: str,
        obj: List[C],
        newline: str = "",
        delimiter: str = ";",
        quotechar: str = '"',
    ) -> None:
        """
        Writes to a csv file format

        Parameters
        -----------
            obj: the object to output to the csv
            file_path : the csv file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)

        """
        with open(file_path, "w", newline=newline) as csvfile:
            writer = csv.writer(
                csvfile, delimiter=delimiter, quotechar=quotechar
            )
            # Header row
            writer.writerow(self.csv_data_schema.header_row_list)
            # Data row
            for row in self.format_object_to_array(obj):
                writer.writerow(row)
        log_event(
            CSVFileWriteSuccessful(
                object_type_name=type(obj).__name__, file_path=file_path
            )
        )

    # Read / Write Methods

    @classmethod
    def _split_cell(cls, input_str: str, delimiter: str = ",") -> list[str]:
        return (
            input_str.split(delimiter)
            if (input_str is not None) | (input_str.strip() != "")
            else []
        )

    @classmethod
    def _get_list_from_single_cell(
        cls, input_str: str, delimiter: str = ","
    ) -> list[str]:
        return [
            entry.strip()
            for entry in input_str.split(delimiter)
            if entry.strip() != ""
        ]

    @classmethod
    def _get_int_from_single_cell(cls, input_str: str) -> Optional[int]:
        return (
            int(input_str)
            if (input_str is not None) & (input_str.strip() != "")
            else None
        )

    @classmethod
    def _get_int_from_bool_single_cell(cls, input_str: str) -> int:
        if input_str is None:
            return False
        if input_str == "":
            return False
        return True if int(input_str) == 1 else False

    @classmethod
    def _get_nullable_string_from_single_cell(
        cls, input_str: str
    ) -> Optional[str]:
        return input_str if input_str != "" else None

    @classmethod
    def _get_str_from_str_single_cell(cls, input_str: str) -> Optional[str]:
        if input_str is None:
            return None
        if input_str.strip() == "":
            return None
        return input_str

    @classmethod
    def _get_tuple_for_name_attributes_from_str_single_cell(
        cls,
        input_dict_str: str,
        attribute_start_char: str = "(",
        attribute_end_char: str = ")",
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        if input_dict_str.find("(") == -1:
            name = input_dict_str
            attributes = None
        else:
            name, attributes_as_str = input_dict_str.split(
                attribute_start_char, 1
            )
            attributes = {}
            if attributes_as_str is not None:
                attributes_as_str = attributes_as_str.replace(
                    attribute_end_char, ""
                )
                attributes = cls._get_dict_from_str_single_cell(
                    attributes_as_str
                )

        return (name, attributes)

    @classmethod
    def _get_dict_from_str_single_cell(cls, input_dict: str) -> Dict[str, Any]:
        attributes: Dict[str, Any] = {}
        if input_dict is None or input_dict == "":
            return attributes
        if input_dict.find(DEFAULT_SEPARATOR_INSIDE_FIELDS_SECOND_LEVEL) == -1:
            key, value = input_dict.split(DEFAULT_SEPARATOR_INSIDE_FIELDS_EQUAL)
            attributes.update({key: value})
        else:
            for attribute in input_dict.split(
                DEFAULT_SEPARATOR_INSIDE_FIELDS_SECOND_LEVEL, 1
            ):
                key, value = attribute.split(
                    DEFAULT_SEPARATOR_INSIDE_FIELDS_EQUAL
                )
                attributes.update({key: value})
        return attributes
