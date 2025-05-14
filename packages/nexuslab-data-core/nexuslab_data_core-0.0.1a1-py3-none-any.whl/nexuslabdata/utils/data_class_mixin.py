import dataclasses
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Self,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

import yaml

from nexuslabdata.exceptions import DataClassReadException
from nexuslabdata.logging import log_event_default
from nexuslabdata.logging.events import (
    DataClassSchemaMissingMandatoryAttribute,
    DataClassSchemaNonAuthorizedAttribute,
    DataClassSchemaSubClassError,
)
from nexuslabdata.utils.mixin import NldMixIn
from nexuslabdata.utils.string_utils import (
    camel_to_snake,
    split_camel_case_string,
)

DATA_CLASS_MIX_IN = TypeVar("DATA_CLASS_MIX_IN", bound="NldDataClassMixIn")
NAMED_DATA_CLASS_MIX_IN = TypeVar(
    "NAMED_DATA_CLASS_MIX_IN", bound="NldNamedDataClassMixIn"
)


class NldDataClassSchema:
    """
    Data Class Schema - General information
    """

    def __init__(
        self,
        schema_class: Type[DATA_CLASS_MIX_IN],
        fields: List[str],
        mandatory_fields: List[str],
        sub_classes_map: Optional[
            Dict[str, Tuple[Type[DATA_CLASS_MIX_IN], type]]
        ] = None,
    ) -> None:
        self.schema_class = schema_class
        self.fields = fields
        self.mandatory_fields = mandatory_fields
        self.sub_classes_map: Dict[
            str, Tuple[Type[DATA_CLASS_MIX_IN], type]
        ] = (sub_classes_map if sub_classes_map is not None else {})
        self._check_coherence()

    @property
    def schema_name(self) -> str:
        return " ".join(split_camel_case_string(self.schema_class.__name__))

    def _check_coherence(self) -> None:
        """
        Checks the coherence of the data class schema.

        Rules checked are :

        - The field list should not be empty
        - The mandatory fields should be included in the authorized fields
        - The keys of the subclass map should be part of the authorized keys
        - The sub classes can only be a dict if there is a name attribute, thus it should be an instance of NldNamedDataClassMixIn

        :return: None. Raises an exception in the event one of the data class schema rules is not met by this instance
        """
        if len(self.fields) == 0:
            raise ValueError("A Data Class Schema requires at least one field.")
        mandatory_field_missing_in_field_list = [
            mandatory_field
            for mandatory_field in self.mandatory_fields
            if mandatory_field not in self.fields
        ]
        if len(mandatory_field_missing_in_field_list) > 0:
            raise ValueError(
                f"All mandatory fields for schema {self.schema_name} should be part of the fields. "
                f"Currently missing fields : {', '.join(mandatory_field_missing_in_field_list)}"
            )
        sub_class_key_missing_in_field_list = [
            sub_class_key
            for sub_class_key in list(self.sub_classes_map.keys())
            if sub_class_key not in self.fields
        ]
        if len(sub_class_key_missing_in_field_list) > 0:
            raise ValueError(
                f"All sub class entries for schema {self.schema_name} should be part of the fields. "
                f"Currently missing fields : {', '.join(sub_class_key_missing_in_field_list)}"
            )
        sub_class_unauthorized_sub_class_type_in_field_list = [
            sub_class_key
            for sub_class_key, (
                sub_class_class,
                sub_class_type,
            ) in self.sub_classes_map.items()
            if (sub_class_type == dict)
            and not (issubclass(sub_class_class, NldNamedDataClassMixIn))
        ]
        if len(sub_class_unauthorized_sub_class_type_in_field_list) > 0:
            raise ValueError(
                f"All sub class entries stored as dictionary should be named data classes. Issue encounterd on {self.schema_name}. "
                f"Un authorized sub classes type : {', '.join(sub_class_unauthorized_sub_class_type_in_field_list)}"
            )

    def check_dict_structure_match(
        self,
        input_dict: Dict[str, Any],
        obj_dict: Optional[Dict[str, Dict[str, DATA_CLASS_MIX_IN]]] = None,
    ) -> bool:
        """
        Checks the coherence of the dictionary for this structure

        Rules checked are :
        - Only authorized fields are present
        - All mandatory keys are provided
        - That all the sub-classes structure match

        :return: True if the provided dictionary matches the structure.
        False otherwise.
        """
        check_status = True
        if type(input_dict) is not dict:
            raise ValueError(
                f"The check dictionary structure requires an input dictionary."
                f" Issue encountered for load of {split_camel_case_string(self.schema_class.__name__)} with an input dict equal to {input_dict} "
            )
        root_level_keys = list(input_dict.keys())
        obj_dict = obj_dict if obj_dict is not None else {}

        # Non Authorized keys check
        non_authorized_keys = [
            root_level_key
            for root_level_key in root_level_keys
            if root_level_key not in self.fields
        ]
        if len(non_authorized_keys) > 0:
            log_event_default(
                DataClassSchemaNonAuthorizedAttribute(
                    self.schema_name, non_authorized_keys
                )
            )
            check_status = False

        # Mandatory fields check
        missing_mandatory_fields = [
            mandatory_field
            for mandatory_field in self.mandatory_fields
            if mandatory_field not in root_level_keys
        ]
        if len(missing_mandatory_fields) > 0:
            log_event_default(
                DataClassSchemaMissingMandatoryAttribute(
                    self.schema_name, missing_mandatory_fields
                )
            )
            check_status = False
        matching_sub_class_keys = [
            sub_class_key
            for sub_class_key in list(self.sub_classes_map.keys())
            if sub_class_key in list(input_dict.keys())
        ]
        for matching_sub_class_key in matching_sub_class_keys:
            sub_class_class, sub_class_type = self.sub_classes_map[
                matching_sub_class_key
            ]
            if sub_class_type == object:
                sub_class_data_matching_structure = (
                    self.check_sub_class_value_match(
                        sub_class_class=sub_class_class,
                        matching_sub_class_key=matching_sub_class_key,
                        sub_class_type=sub_class_type,
                        sub_class_value=input_dict[matching_sub_class_key],
                        obj_dict=obj_dict,
                    )
                )
            elif sub_class_type == list:
                sub_class_data_matching_structure = True
                for sub_class_list_entry in input_dict[matching_sub_class_key]:
                    if not self.check_sub_class_value_match(
                        sub_class_class=sub_class_class,
                        matching_sub_class_key=matching_sub_class_key,
                        sub_class_type=sub_class_type,
                        sub_class_value=sub_class_list_entry,
                        obj_dict=obj_dict,
                    ):
                        sub_class_data_matching_structure = False
            elif sub_class_type == dict:
                sub_class_data_matching_structure = True
                for sub_class_list_key, sub_class_list_value in input_dict[
                    matching_sub_class_key
                ].items():
                    if not self.check_sub_class_value_match(
                        sub_class_class=sub_class_class,
                        matching_sub_class_key=matching_sub_class_key,
                        sub_class_type=sub_class_type,
                        sub_class_value=sub_class_list_value,
                        obj_dict=obj_dict,
                    ):
                        sub_class_data_matching_structure = False
            else:
                raise ValueError(
                    f"Sub Class content provided for key : {matching_sub_class_key} is not allowed / Type provided is : {sub_class_type.__name__}"
                )

            if not sub_class_data_matching_structure:
                log_event_default(
                    DataClassSchemaSubClassError(
                        self.schema_name,
                        matching_sub_class_key,
                        sub_class_class.__name__,
                    )
                )

        return check_status

    def check_sub_class_value_match(
        self,
        sub_class_class: Type[DATA_CLASS_MIX_IN],
        matching_sub_class_key: str,
        sub_class_type: type,
        sub_class_value: Union[str, Dict[str, Any]],
        obj_dict: Optional[Dict[str, Dict[str, DATA_CLASS_MIX_IN]]] = None,
    ) -> bool:
        if sub_class_value is None:
            # Check if the field is optional
            field_info = next(
                (
                    f
                    for f in dataclasses.fields(self.schema_class)
                    if f.name == matching_sub_class_key
                ),
                None,
            )
            if (
                field_info
                and get_origin(field_info.type) is Union
                and type(None) in get_args(field_info.type)
            ):
                return True
            raise ValueError(
                f"The content of sub class {matching_sub_class_key} cannot be None for non-optional field"
            )

        if isinstance(sub_class_value, str):
            sub_class_data_matching_structure = (
                self.check_sub_class_object_available_for_name(
                    sub_class_class,
                    matching_sub_class_key,
                    sub_class_value,
                    obj_dict=obj_dict,
                )
            )
        else:
            if type(sub_class_value) is not dict:
                raise ValueError(
                    f"The content of sub class {matching_sub_class_key} for each entry should be a dictionary "
                    f"but is of type {str(type(sub_class_value))}"
                )
            sub_class_data_matching_structure = sub_class_class.get_data_class_schema().check_dict_structure_match(
                input_dict=sub_class_value, obj_dict=obj_dict
            )
        return sub_class_data_matching_structure

    def check_sub_class_object_available_for_name(
        self,
        sub_class_class: type,
        matching_sub_class_key: str,
        sub_class_key_name: str,
        obj_dict: Optional[Dict[str, Dict[str, DATA_CLASS_MIX_IN]]] = None,
    ) -> bool:
        obj_dict = obj_dict if obj_dict is not None else {}
        sub_class_type_key_name_in_dict = camel_to_snake(
            sub_class_class.__name__
        )
        if sub_class_type_key_name_in_dict not in obj_dict:
            sub_class_independent_att = next(
                (
                    f
                    for f in dataclasses.fields(sub_class_class)
                    if f.name == "INDEPENDENT"
                ),
                None,
            )
            if sub_class_independent_att is not None:
                if sub_class_independent_att.default:
                    raise ValueError(
                        f"Objects {camel_to_snake(sub_class_class.__name__)} are not available for object creation."
                    )
        sub_class_objects = obj_dict[sub_class_type_key_name_in_dict]
        if sub_class_key_name not in list(sub_class_objects.keys()):
            raise ValueError(
                f"No object with name {sub_class_key_name} is available for sub class {matching_sub_class_key}"
            )
        return True


@dataclasses.dataclass
class NldDataClassMixIn(NldMixIn):
    """MixIn for all the NLD data classes.

    Initializes the local logger.
    Provides methods to read/write in YAML
    """

    # Indicates if the object can be instantiated independently
    INDEPENDENT: bool = dataclasses.field(default=True, init=False)

    def __post_init__(self) -> None:
        self._init_logger()

    @classmethod
    def data_class_name(cls) -> str:
        return " ".join(split_camel_case_string(cls.__name__))

    @classmethod
    def from_yaml(
        cls,
        yaml_content: str,
        obj_dict: Optional[Dict[str, Dict[str, DATA_CLASS_MIX_IN]]] = None,
    ) -> Self:
        return cls.from_dict(yaml.safe_load(yaml_content), obj_dict=obj_dict)

    @classmethod
    def from_dict(
        cls,
        from_dict: Dict[str, Any],
        obj_dict: Optional[Dict[str, Dict[str, DATA_CLASS_MIX_IN]]] = None,
    ) -> Self:
        data_class_schema = cls.get_data_class_schema()
        structure_match = data_class_schema.check_dict_structure_match(
            from_dict, obj_dict=obj_dict
        )
        if not structure_match:
            raise DataClassReadException(
                data_class_name=cls.data_class_name(), method_name="from_dict"
            )
        return cls.adapt_dict_to_object(from_dict, obj_dict=obj_dict)

    def to_dict(self) -> Dict[str, Any]:
        data_class_schema = self.get_data_class_schema()
        new_dict = {}
        for field_name in data_class_schema.fields:
            if not (field_name in data_class_schema.sub_classes_map.keys()):
                new_dict[field_name] = getattr(self, field_name)
            else:
                (
                    sub_class_class,
                    sub_class_type,
                ) = data_class_schema.sub_classes_map[field_name]

                if sub_class_type == object:
                    cur_value = cast(
                        NldDataClassMixIn, getattr(self, field_name)
                    )
                    new_dict[field_name] = cur_value.to_dict()

                elif sub_class_type == list:
                    cur_list_value = cast(
                        List[NldDataClassMixIn], getattr(self, field_name)
                    )
                    current_list = []
                    for list_entry in cur_list_value:
                        current_list.append(list_entry.to_dict())
                    new_dict[field_name] = current_list
                elif sub_class_type == dict:
                    cur_dict_value = cast(
                        Dict[str, NldDataClassMixIn], getattr(self, field_name)
                    )
                    new_sub_class_dict = {}
                    for dict_key, dict_value in cur_dict_value.items():
                        new_sub_class_dict[dict_key] = dict_value.to_dict()
                    new_dict[field_name] = new_sub_class_dict
        return new_dict

    @classmethod
    def adapt_dict_to_object(
        cls,
        raw_dict: Dict[str, Any],
        obj_dict: Optional[Dict[str, Dict[str, DATA_CLASS_MIX_IN]]] = None,
    ) -> Self:
        if raw_dict is None:
            return None  # return None if fields are optional champs optionnel

        new_dict = {}
        obj_dict = obj_dict if obj_dict is not None else {}
        data_class_schema = cls.get_data_class_schema()

        # Validate the keys on the schema
        valid_keys = set(data_class_schema.sub_classes_map.keys()) | set(
            data_class_schema.fields
        )
        invalid_keys = set(raw_dict.keys()) - valid_keys
        if invalid_keys:
            raise DataClassReadException(
                data_class_name=cls.__name__, method_name="adapt_dict_to_object"
            )

        for key, value in raw_dict.items():
            if key not in data_class_schema.sub_classes_map:
                new_dict[key] = value
            else:
                (
                    sub_class_class,
                    sub_class_type,
                ) = data_class_schema.sub_classes_map[key]
                sub_class_data_schema = sub_class_class.get_data_class_schema()

                if sub_class_type == object:
                    new_dict[key] = cls.adapt_sub_class(
                        sub_class_data_schema, value, obj_dict
                    )
                elif sub_class_type == list:
                    current_list = []
                    for list_entry in value:
                        current_list.append(
                            cls.adapt_sub_class(
                                sub_class_data_schema, list_entry, obj_dict
                            )
                        )
                    new_dict[key] = current_list
                else:
                    if sub_class_type == dict:
                        new_sub_class_dict = {}
                        for dict_key, dict_value in value.items():
                            new_sub_class_dict[dict_key] = cls.adapt_sub_class(
                                sub_class_data_schema, dict_value, obj_dict
                            )
                        new_dict[key] = new_sub_class_dict
        return cls(**new_dict)

    @classmethod
    def adapt_sub_class(
        cls,
        sub_class_data_schema: NldDataClassSchema,
        value: Union[str, Dict[str, Any]],
        obj_dict: Dict[str, Dict[str, DATA_CLASS_MIX_IN]],
    ) -> DATA_CLASS_MIX_IN:
        if isinstance(value, str):
            obj = obj_dict[
                camel_to_snake(sub_class_data_schema.schema_class.__name__)
            ][value]
            return sub_class_data_schema.schema_class.deep_copy(obj)
        return sub_class_data_schema.schema_class.adapt_dict_to_object(
            value, obj_dict=obj_dict
        )

    @classmethod
    def get_data_class_schema(cls) -> NldDataClassSchema:
        fields: List[str] = []
        mandatory_fields: List[str] = []
        sub_classes_map: Dict[str, Tuple[Type["NldDataClassMixIn"], type]] = {}

        # All upper case attributes are considered Data Class level
        # and not to be considered in the Data Class Schema
        data_class_fields = [
            f
            for f in dataclasses.fields(cls)
            if not (
                f.name.isupper()
                and all(c.isalpha() or c == "_" for c in f.name)
            )
        ]
        for lcl_field in data_class_fields:
            field_name = lcl_field.name
            field_type = lcl_field.type
            field_default = lcl_field.default
            fields.append(field_name)
            if not (
                get_origin(field_type) is Union
                and type(None) in get_args(field_type)
            ):  # Field is mandatory (not optional)
                if field_default is dataclasses.MISSING:
                    mandatory_fields.append(field_name)

            # Determine sub classes map
            if get_origin(field_type) is Union:
                non_none_args = [
                    arg for arg in get_args(field_type) if arg is not None
                ]
                field_cleaned_type = non_none_args[0]
            else:
                field_cleaned_type = field_type

            if get_origin(field_cleaned_type) is dict:
                dict_key_class, dict_value_class = get_args(field_cleaned_type)
                if isinstance(dict_value_class, type):
                    if issubclass(dict_value_class, NldDataClassMixIn):
                        sub_classes_map[field_name] = (dict_value_class, dict)
            elif get_origin(field_cleaned_type) is list:
                list_value_class = get_args(field_cleaned_type)[0]
                if get_origin(list_value_class) is dict:
                    dict_key_class, dict_value_class = get_args(
                        list_value_class
                    )
                    if issubclass(dict_value_class, NldDataClassMixIn):
                        sub_classes_map[field_name] = (dict_value_class, dict)
                elif issubclass(list_value_class, NldDataClassMixIn):
                    sub_classes_map[field_name] = (list_value_class, list)
            elif get_origin(field_cleaned_type) is Literal:
                # If literal is provided, the data is considered as a string
                pass
            elif issubclass(field_cleaned_type, NldDataClassMixIn):
                sub_classes_map[field_name] = (field_cleaned_type, object)

        return NldDataClassSchema(
            cls, fields, mandatory_fields, sub_classes_map
        )

    def as_dict(self) -> Dict[str, Any]:
        # All upper case attributes are removed from this standard as_dict to represent only non level class attributes
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if not (k.isupper() and all(c.isalpha() or c == "_" for c in k))
        }


@dataclasses.dataclass
class NldNamedDataClassMixIn(NldDataClassMixIn):
    """MixIn for all the NLD named data classes.

    Contains a name for the identification
    """

    name: str
