import os
from typing import Any, Dict, Optional, Type

from nexuslabdata.exceptions import DataClassReadException
from nexuslabdata.logging import (
    StandardDebugEvent,
    StandardTestEvent,
    log_event_default,
)
from nexuslabdata.service.events import (
    DataClassReadFromDirectoryCompletedSuccessfullyEvent,
    DataClassReadFromDirectoryStartEvent,
)
from nexuslabdata.utils import file_util
from nexuslabdata.utils.data_class_mixin import NAMED_DATA_CLASS_MIX_IN
from nexuslabdata.utils.file_util import load_file_into_dict
from nexuslabdata.utils.jinja_utils import JINJA2_FILE_STANDARD_REGEX
from nexuslabdata.utils.yaml_util import (
    YAML_FILE_STANDARD_REGEX,
    load_yaml_file_into_dict,
)


def read_objects_from_local_directory(
    data_class: Type[NAMED_DATA_CLASS_MIX_IN],
    root_path: str,
    obj_dict: Optional[Dict[str, Dict[str, NAMED_DATA_CLASS_MIX_IN]]] = None,
) -> Dict[str, NAMED_DATA_CLASS_MIX_IN]:
    definitions: Dict[str, NAMED_DATA_CLASS_MIX_IN] = {}
    log_event_default(
        DataClassReadFromDirectoryStartEvent(
            data_class=data_class, root_path=root_path
        )
    )
    for file_path in file_util.get_list_of_files_in_cur_folder(
        root_path, YAML_FILE_STANDARD_REGEX
    ):
        try:
            definition = data_class.from_dict(
                load_yaml_file_into_dict(file_path), obj_dict=obj_dict
            )
            definitions.update({definition.name: definition})
        except DataClassReadException as e:
            log_event_default(
                StandardDebugEvent(
                    f"Error on the {data_class.get_data_class_schema().schema_name} file : {os.path.basename(file_path)}"
                )
            )
            raise e
    log_event_default(
        StandardTestEvent(
            f"{data_class.get_data_class_schema().schema_name} loaded are : {', '.join(list(definitions.keys()))}"
        )
    )
    log_event_default(
        DataClassReadFromDirectoryCompletedSuccessfullyEvent(
            data_class=data_class
        )
    )
    return definitions


def read_files_from_local_directory(
    data_class: Type[NAMED_DATA_CLASS_MIX_IN],
    root_path: str,
    obj_dict: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Reads files from a local directory and returns a dictionary of instances created from the files.

    Parameters
    -----------
    data_class : Type[Any]
        The data class that implements a from_dict method.

    root_path : str
        The root directory where to search for files.

    obj_dict : Optional[Dict[str, Dict[str, Any]]]
        An optional dictionary passed to the from_dict method.

    Returns
    -----------
    Dict[str, Any]
        A dictionary with keys as instance names and values as instances created from file content.

    """
    definitions: Dict[str, Any] = {}
    log_event_default(
        DataClassReadFromDirectoryStartEvent(
            data_class=data_class, root_path=root_path
        )
    )
    for file_path in file_util.get_list_of_files_in_cur_folder(
        root_path, JINJA2_FILE_STANDARD_REGEX
    ):
        try:
            file_dict = load_file_into_dict(file_path)
            key, content = next(iter(file_dict.items()))

            init_dict = {"name": key, "template": content}
            instance = data_class.from_dict(init_dict, obj_dict=obj_dict)
            definitions[instance.name] = instance
        except DataClassReadException as e:
            log_event_default(
                StandardDebugEvent(
                    f"Error on the {data_class.get_data_class_schema().schema_name} file : {os.path.basename(file_path)}"
                )
            )
            raise e
    log_event_default(
        StandardTestEvent(
            f"{data_class.get_data_class_schema().schema_name} loaded are : {', '.join(list(definitions.keys()))}"
        )
    )
    log_event_default(
        DataClassReadFromDirectoryCompletedSuccessfullyEvent(
            data_class=data_class
        )
    )
    return definitions
