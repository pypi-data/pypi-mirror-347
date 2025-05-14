import abc
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union

from nexuslabdata.exceptions import NotImplementedMethodException

DEFAULT_SEPARATOR = ";"
DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL = "|"
DEFAULT_SEPARATOR_INSIDE_FIELDS_SECOND_LEVEL = ","
DEFAULT_SEPARATOR_INSIDE_FIELDS_EQUAL = "="

C = TypeVar("C", bound=Any)


class BaseFlattenAdapter(Generic[C], metaclass=abc.ABCMeta):
    @classmethod
    def _flatten_in_single_cell_dict(
        cls, input_dict: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        return (
            DEFAULT_SEPARATOR_INSIDE_FIELDS_FIRST_LEVEL.join(
                [
                    f"{key}{DEFAULT_SEPARATOR_INSIDE_FIELDS_EQUAL}{value}"
                    for key, value in input_dict.items()
                ]
            )
            if input_dict is not None
            else None
        )


class ObjectFlattenAdapter(BaseFlattenAdapter[C], metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def flatten(cls, obj: C) -> Tuple[Optional[Union[int, str]], ...]:
        raise NotImplementedMethodException(cls, "flatten")


class ListFlattenAdapter(BaseFlattenAdapter[C], metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def flatten(cls, obj: C) -> List[Tuple[Optional[Union[int, str]], ...]]:
        raise NotImplementedMethodException(cls, "flatten")
