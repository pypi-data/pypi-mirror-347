import os
from typing import Dict, List, cast

from nexuslabdata.core import Field, Structure, StructureAdapter
from nexuslabdata.core.flow import DataFlowExecution
from nexuslabdata.core.structure.sql_renderer_wrapper import SQLRendererWrapper
from nexuslabdata.core.structure.sql_template_wrapper import SQLTemplateWrapper
from nexuslabdata.service.config_service import ConfigService
from nexuslabdata.service.data_flow_service import (
    DataFlowObjectNames,
    DataFlowService,
)
from nexuslabdata.service.model_service import ModelObjectNames, ModelService
from nexuslabdata.service.structure_service import (
    StructureObjectNames,
    StructureService,
)


class NldServiceWrapper:
    def __init__(
        self,
        config_service: ConfigService,
        model_service: ModelService,
        structure_service: StructureService,
        data_flow_service: DataFlowService,
    ):
        self.config_service = config_service
        self.model_service = model_service
        self.structure_service = structure_service
        self.data_flow_service = data_flow_service

    def get_field_dict(self) -> Dict[str, Field]:
        return cast(
            Dict[str, Field],
            self.model_service.get_dict(ModelObjectNames.FIELD.value),
        )

    def get_field_keys(self) -> List[str]:
        return self.model_service.get_object_keys(ModelObjectNames.FIELD.value)

    def get_field(self, object_key: str) -> Field:
        return cast(
            Field,
            self.model_service.get_object(
                ModelObjectNames.FIELD.value, object_key
            ),
        )

    def get_fields(self, object_keys: List[str]) -> List[Field]:
        return cast(
            List[Field],
            self.model_service.get_objects(
                ModelObjectNames.FIELD.value, object_keys
            ),
        )

    def get_fields_as_dict(self, object_keys: List[str]) -> Dict[str, Field]:
        return cast(
            Dict[str, Field],
            self.model_service.get_objects_as_dict(
                ModelObjectNames.FIELD.value, object_keys
            ),
        )

    # structure adapter in model
    def get_structure_adapter_dict(self) -> Dict[str, StructureAdapter]:
        return cast(
            Dict[str, StructureAdapter],
            self.model_service.get_dict(
                ModelObjectNames.STRUCTURE_ADAPTER.value
            ),
        )

    def get_structure_adapter_keys(self) -> List[str]:
        return self.model_service.get_object_keys(
            ModelObjectNames.STRUCTURE_ADAPTER.value
        )

    def get_structure_adapter(self, object_key: str) -> StructureAdapter:
        return cast(
            StructureAdapter,
            self.model_service.get_object(
                ModelObjectNames.STRUCTURE_ADAPTER.value, object_key
            ),
        )

    def get_structure_adapters(
        self, object_keys: List[str]
    ) -> List[StructureAdapter]:
        return cast(
            List[StructureAdapter],
            self.model_service.get_objects(
                ModelObjectNames.STRUCTURE_ADAPTER.value, object_keys
            ),
        )

    def get_structure_adapters_as_dict(
        self, object_keys: List[str]
    ) -> Dict[str, StructureAdapter]:
        return cast(
            Dict[str, StructureAdapter],
            self.model_service.get_objects_as_dict(
                ModelObjectNames.STRUCTURE_ADAPTER.value, object_keys
            ),
        )

    # sql renderer in model
    def get_sql_renderer_dict(self) -> Dict[str, SQLRendererWrapper]:
        return cast(
            Dict[str, SQLRendererWrapper],
            self.model_service.get_dict(ModelObjectNames.SQL_RENDERER.value),
        )

    def get_sql_renderer_keys(self) -> List[str]:
        return self.model_service.get_object_keys(
            ModelObjectNames.SQL_RENDERER.value
        )

    def get_sql_renderer(self, object_key: str) -> SQLRendererWrapper:
        return cast(
            SQLRendererWrapper,
            self.model_service.get_object(
                ModelObjectNames.SQL_RENDERER.value, object_key
            ),
        )

    def get_sql_renderers(
        self, object_keys: List[str]
    ) -> List[SQLRendererWrapper]:
        return cast(
            List[SQLRendererWrapper],
            self.model_service.get_objects(
                ModelObjectNames.SQL_RENDERER.value, object_keys
            ),
        )

    def get_sql_renderers_as_dict(
        self, object_keys: List[str]
    ) -> Dict[str, SQLRendererWrapper]:
        return cast(
            Dict[str, SQLRendererWrapper],
            self.model_service.get_objects_as_dict(
                ModelObjectNames.SQL_RENDERER.value, object_keys
            ),
        )

    # sql template in model
    def get_sql_template_dict(self) -> Dict[str, SQLTemplateWrapper]:
        return cast(
            Dict[str, SQLTemplateWrapper],
            self.model_service.get_dict(ModelObjectNames.SQL_TEMPLATE.value),
        )

    def get_sql_template_keys(self) -> List[str]:
        return self.model_service.get_object_keys(
            ModelObjectNames.SQL_TEMPLATE.value
        )

    def get_sql_template(self, object_key: str) -> SQLTemplateWrapper:
        return cast(
            SQLTemplateWrapper,
            self.model_service.get_object(
                ModelObjectNames.SQL_TEMPLATE.value, object_key
            ),
        )

    def get_sql_templates(
        self, object_keys: List[str]
    ) -> List[SQLTemplateWrapper]:
        return cast(
            List[SQLTemplateWrapper],
            self.model_service.get_objects(
                ModelObjectNames.SQL_TEMPLATE.value, object_keys
            ),
        )

    def get_sql_templates_as_dict(
        self, object_keys: List[str]
    ) -> Dict[str, SQLTemplateWrapper]:
        return cast(
            Dict[str, SQLTemplateWrapper],
            self.model_service.get_objects_as_dict(
                ModelObjectNames.SQL_TEMPLATE.value, object_keys
            ),
        )

    # Structure
    def get_structure_dict(self) -> Dict[str, Structure]:
        return cast(
            Dict[str, Structure],
            self.structure_service.get_dict(
                StructureObjectNames.STRUCTURE.value
            ),
        )

    def get_structure_keys(self) -> List[str]:
        return self.structure_service.get_object_keys(
            StructureObjectNames.STRUCTURE.value
        )

    def get_structure(self, object_key: str) -> Structure:
        return cast(
            Structure,
            self.structure_service.get_object(
                StructureObjectNames.STRUCTURE.value, object_key
            ),
        )

    def get_structures(self, object_keys: List[str]) -> List[Structure]:
        return cast(
            List[Structure],
            self.structure_service.get_objects(
                StructureObjectNames.STRUCTURE.value, object_keys
            ),
        )

    def get_structures_as_dict(
        self, object_keys: List[str]
    ) -> Dict[str, Structure]:
        return cast(
            Dict[str, Structure],
            self.structure_service.get_objects_as_dict(
                StructureObjectNames.STRUCTURE.value, object_keys
            ),
        )

    # DataFlow methods
    def get_data_flow_execution_dict(self) -> Dict[str, DataFlowExecution]:
        return cast(
            Dict[str, DataFlowExecution],
            self.data_flow_service.get_dict(
                DataFlowObjectNames.DATA_FLOW_EXECUTION.value
            ),
        )

    def get_data_flow_execution_keys(self) -> List[str]:
        return self.data_flow_service.get_object_keys(
            DataFlowObjectNames.DATA_FLOW_EXECUTION.value
        )

    def get_data_flow_execution(self, object_key: str) -> DataFlowExecution:
        return cast(
            DataFlowExecution,
            self.data_flow_service.get_object(
                DataFlowObjectNames.DATA_FLOW_EXECUTION.value, object_key
            ),
        )

    def get_data_flows(self, object_keys: List[str]) -> List[DataFlowExecution]:
        return cast(
            List[DataFlowExecution],
            self.data_flow_service.get_objects(
                DataFlowObjectNames.DATA_FLOW_EXECUTION.value, object_keys
            ),
        )

    def get_data_flows_as_dict(
        self, object_keys: List[str]
    ) -> Dict[str, DataFlowExecution]:
        return cast(
            Dict[str, DataFlowExecution],
            self.data_flow_service.get_objects_as_dict(
                DataFlowObjectNames.DATA_FLOW_EXECUTION.value, object_keys
            ),
        )


def create_nld_service_wrapper(
    root_folder_path: str,
    config_folder_name: str,
    model_folder_name: str,
    structure_folder_name: str,
    data_flow_folder_name: str,
    load_obj_service: bool = True,
) -> NldServiceWrapper:
    config_service = ConfigService()
    model_service = ModelService()
    structure_service = StructureService()
    data_flow_service = DataFlowService()

    if load_obj_service:
        config_service.load_objects(
            root_directory=os.path.join(root_folder_path, config_folder_name)
        )
        model_service.load_objects(
            root_directory=os.path.join(root_folder_path, model_folder_name)
        )
        structure_service.load_objects(
            root_directory=os.path.join(root_folder_path, structure_folder_name)
        )
        data_flow_service.load_objects(
            root_directory=os.path.join(root_folder_path, data_flow_folder_name)
        )

    return NldServiceWrapper(
        config_service=config_service,
        model_service=model_service,
        structure_service=structure_service,
        data_flow_service=data_flow_service,
    )
