from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from nexuslabdata.core.flow.definition.tfm.target_from_source_mapping import (
    TargetFromSourceMappingDefinition,
)
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FlowTransformationDefinition(NldDataClassMixIn):
    name: str
    attributes: Optional[Dict[str, str]] = None
    target_from_source_mapping: Optional[List[Dict[str, Any]]] = None
    predecessors: Optional[List[str]] = None

    def get_target_from_source_mapping_list(
        self,
    ) -> List[TargetFromSourceMappingDefinition]:
        target_from_source_mapping_definition_list: List[
            TargetFromSourceMappingDefinition
        ] = []
        if self.target_from_source_mapping is None:
            return target_from_source_mapping_definition_list
        for target_from_source_mapping in self.target_from_source_mapping:
            for key, value in target_from_source_mapping.items():
                target_field_name = key
                source_field_name = None
                function_name = None
                formula = None
                if isinstance(value, str):
                    source_field_name = value
                elif isinstance(value, dict):
                    source_field_name = (
                        value["source_field_name"]
                        if "source_field_name" in list(value.keys())
                        else None
                    )
                    function_name = (
                        value["function_name"]
                        if "function_name" in list(value.keys())
                        else None
                    )
                    formula = (
                        value["formula"]
                        if "formula" in list(value.keys())
                        else None
                    )

                target_from_source_mapping_definition_list.append(
                    TargetFromSourceMappingDefinition(
                        target_field_name=target_field_name,
                        source_field_name=source_field_name,
                        function_name=function_name,
                        formula=formula,
                    )
                )

        return target_from_source_mapping_definition_list

    def get_target_from_source_mapping_dict(
        self,
    ) -> Dict[str, TargetFromSourceMappingDefinition]:
        return {
            mapping.target_field_name: mapping
            for mapping in self.get_target_from_source_mapping_list()
            if mapping.target_field_name is not None
        }
