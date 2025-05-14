import os.path
from typing import Any, Dict, List, Optional, Type

from nexuslabdata.logging import NldLoggable
from nexuslabdata.service.data_class_read_util import (
    read_files_from_local_directory,
    read_objects_from_local_directory,
)
from nexuslabdata.service.exceptions import ObjectReadNoDirectoryException
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn
from nexuslabdata.utils.string_utils import un_camel


class ObjectDefinition(NldLoggable):
    def __init__(
        self,
        name: str,
        data_class: Type[NldNamedDataClassMixIn],
        folder_name: str,
        file_format: str = "yaml",
    ):
        super().__init__()
        if file_format not in ["yaml", "jinja"]:
            raise ValueError(
                "Invalid file_format: file_format must be one of ['yaml', 'jinja']"
            )
        self.name = name
        self.data_class = data_class
        self.folder_name = folder_name
        self.file_format = file_format

    def get_data_class_name(self) -> str:
        return un_camel(self.data_class.__name__)


class ObjectStandardProviderService(NldLoggable):
    """
    Standard Object Provider Service

    Stores all the objects and provides standard methods to retrieve all the objects
    """

    def __init__(self, object_definitions: List[ObjectDefinition]) -> None:
        super().__init__()
        self.object_definitions: List[ObjectDefinition] = object_definitions
        self.objects: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def get_object_definition(
        self, object_name: str
    ) -> Optional[ObjectDefinition]:
        matching_object_definitions = [
            obj_def
            for obj_def in self.object_definitions
            if obj_def.name == object_name
        ]
        return (
            matching_object_definitions[0]
            if len(matching_object_definitions) > 0
            else None
        )

    def replace_object_type_objects(
        self, key: str, obj_dict: Dict[str, Any]
    ) -> None:
        self.objects.update({key: obj_dict})

    def get_available_object_types(self) -> List[str]:
        """
        Get all the available object types.

        Returns
        -----------
            The string-list of object types
        """
        return list(self.objects.keys())

    def get_object_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the complete object Dictionary.

        The dictionary associates a object type name (key) to a dictionary
        containing all the objects stored with a key name

        Returns
        -----------
            The object dictionary
        """
        return self.objects

    def get_dict(self, object_type: str) -> Dict[str, Any]:
        """
        Get a key-value dictionary for the object type provided.

        The key is the name of the object and the value can be
        of any type but always the same throughout the dictionary.

        Parameters
        -----------
            object_type : the name of the object type

        Returns
        -----------
            The object type dictionary
        """
        return (
            self.objects[object_type]
            if object_type in self.objects.keys()
            else {}
        )

    def get_object_keys(self, object_type: str) -> List[str]:
        """
        Get the list of keys for the object type provided.

        Parameters
        -----------
            object_type : the name of the object type

        Returns
        -----------
            The list of keys for the object type provided
        """
        return list(self.get_dict(object_type).keys())

    def get_object(self, object_type: str, object_key: str) -> Any:
        """
        Get the object of type object_type and with name equal to the object_key

        Parameters
        -----------
            object_type : the name of the object type
            object_key : the key (name) of the object

        Returns
        -----------
            A stored object
        """
        obj_type_dict = self.get_dict(object_type=object_type)
        if obj_type_dict is None:
            raise ValueError("No Object Type stored with name : " + object_type)
        return (
            obj_type_dict[object_key]
            if object_key in obj_type_dict.keys()
            else None
        )

    def get_objects(
        self, object_type: str, object_keys: List[str]
    ) -> List[Any]:
        """
        Get the list of objects of type object_type and with the object keys (names) as provided

        Parameters
        -----------
            object_type : the name of the object type
            object_keys : the list of keys (names) of the objects to look for

        Returns
        -----------
            The list of stored objects with the provided keys
        """
        obj_type_dict = self.get_dict(object_type=object_type)
        if obj_type_dict is None:
            raise ValueError("No Object Type stored with name : " + object_type)
        return [
            obj_type_dict[key]
            for key in object_keys
            if key in obj_type_dict.keys()
        ]

    def get_objects_as_dict(
        self, object_type: str, object_keys: List[str]
    ) -> Dict[str, Any]:
        """
        Get the list of objects of type object_type and with the object keys (names) as provided in a dict format

        Parameters
        -----------
            object_type : the name of the object type
            object_keys : the list of keys (names) of the objects to look for

        Returns
        -----------
            The list of stored objects with the provided keys as a dictionary with as key the object name/key
        """
        obj_type_dict = self.get_dict(object_type=object_type)
        if obj_type_dict is None:
            raise ValueError("No Object Type stored with name : " + object_type)
        return {
            key: obj_type_dict[key]
            for key in object_keys
            if key in obj_type_dict.keys()
        }

    def load_objects(
        self,
        root_directory: str,
        fail_on_missing_folder: bool = False,
    ) -> None:
        for object_definition in self.object_definitions:
            self.load_from_object_definition(
                root_directory, object_definition, fail_on_missing_folder
            )

    def load_from_object_definition(
        self,
        root_directory: str,
        obj_definition: ObjectDefinition,
        fail_on_missing_folder: bool,
    ) -> None:
        object_folder_path = os.path.join(
            root_directory, obj_definition.folder_name
        )
        if not os.path.exists(object_folder_path):
            if fail_on_missing_folder:
                raise ObjectReadNoDirectoryException(
                    folder_path=object_folder_path,
                    data_class=obj_definition.data_class,
                )
            else:
                self.replace_object_type_objects(obj_definition.name, {})
        else:
            if obj_definition.file_format == "yaml":
                loaded: Dict[str, Any] = read_objects_from_local_directory(
                    obj_definition.data_class, object_folder_path, self.objects
                )
            else:
                loaded = read_files_from_local_directory(
                    obj_definition.data_class, object_folder_path, self.objects
                )

            self.replace_object_type_objects(obj_definition.name, loaded)
