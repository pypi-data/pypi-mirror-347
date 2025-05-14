import abc
from dataclasses import dataclass
from typing import TypeVar


@dataclass
class BaseConnectionCredential(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError(
            "The type method is not implemented for class : " + str(type(self))
        )


@dataclass
class BaseSqlCredential(BaseConnectionCredential, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError(
            "The type method is not implemented for class : " + str(type(self))
        )


CREDENTIAL_TYPE = TypeVar("CREDENTIAL_TYPE", bound=BaseConnectionCredential)
