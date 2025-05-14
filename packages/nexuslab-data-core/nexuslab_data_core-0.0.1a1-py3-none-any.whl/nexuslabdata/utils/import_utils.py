import importlib
from types import ModuleType
from typing import Any, Tuple, Type

from nexuslabdata.logging.logger import log_debug_default


def import_class_inside_module(class_path: str) -> Tuple[ModuleType, Type[Any]]:
    log_debug_default(f"Import of class {class_path} - Started")
    if "." in class_path:
        module_name, class_name = class_path.rsplit(".", 1)
    else:
        raise RuntimeError(
            f"Class should be contained inside a module, but only the name was provided ${class_path}"
        )

    module = importlib.import_module(module_name)
    class_type = getattr(module, class_name)

    log_debug_default(f"Import of class {class_path} - Completed successfully")

    return module, class_type
