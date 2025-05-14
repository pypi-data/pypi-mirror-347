from typing import Any, Dict

import yaml
from yaml import MappingNode, SafeDumper, ScalarNode

YAML_FILE_STANDARD_REGEX = r".*\.yml$"


def load_yaml_file_into_dict(file_path: str) -> Any:
    """
    Loads a yaml file into a dictionary

    Parameters
    ----------
    file_path : The local file path

    Returns
    -------
    A dictionary loaded with all the yaml file content
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def quoted_presenter(dumper: "QuotedValuesDumper", data: str) -> ScalarNode:
    """
    Represent string values as single-quoted in YAML.
    """
    return ScalarNode(tag="tag:yaml.org,2002:str", value=data, style="'")


def represent_mapping_without_quoted_keys(
    dumper: "QuotedValuesDumper", data: Dict[str, Any]
) -> MappingNode:
    """
    Represent dict mappings so that:
      - keys are plain (no quotes)
      - string values use the quoted_presenter
    """
    node_values = []
    for key, val in data.items():
        key_node = dumper.represent_data(key)
        key_node.style = None  # type: ignore[attr-defined]
        val_node = dumper.represent_data(val)
        node_values.append((key_node, val_node))
    return MappingNode(
        tag="tag:yaml.org,2002:map", value=node_values, flow_style=False
    )


class QuotedValuesDumper(SafeDumper):
    """
    YAML Dumper subclass that:
      - single-quotes all string values
      - never quotes mapping keys
    """


QuotedValuesDumper.add_representer(str, quoted_presenter)
QuotedValuesDumper.add_representer(dict, represent_mapping_without_quoted_keys)


def dump_dict_to_yaml(
    data: Dict[str, Any],
    file_path: str,
    *,
    sort_keys: bool = False,
    allow_unicode: bool = True,
    default_flow_style: bool = False,
) -> None:
    """
    Dump a Python dict to a YAML file with custom formatting:
      - mapping keys are unquoted
      - string values are single-quoted
    """
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            Dumper=QuotedValuesDumper,
            sort_keys=sort_keys,
            allow_unicode=allow_unicode,
            default_flow_style=default_flow_style,
        )
