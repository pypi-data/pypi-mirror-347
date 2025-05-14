from typing import Any, Callable, Union

_STD_CALLABLE = Callable[[Any], Any]
_ALL_CALLABLES = Union[_STD_CALLABLE, Any]


def composed(
    *decs: Union[_ALL_CALLABLES, tuple[_ALL_CALLABLES]]
) -> Callable[[Any], Any]:
    def deco(f: Callable[[Any], Any]) -> Callable[[Any], Any]:
        for dec in reversed(decs):
            f = dec(f)  # type: ignore
        return f

    return deco
