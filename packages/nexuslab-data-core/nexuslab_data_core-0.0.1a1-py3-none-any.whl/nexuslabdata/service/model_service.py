from nexuslabdata.core import Field, FieldTemplate
from nexuslabdata.core.field.field_adapter import FieldAdapter
from nexuslabdata.core.field.field_format_adapter import FieldFormatAdapter
from nexuslabdata.core.structure.sql_renderer_wrapper import SQLRendererWrapper
from nexuslabdata.core.structure.sql_template_wrapper import SQLTemplateWrapper
from nexuslabdata.core.structure.structure_adapter import StructureAdapter
from nexuslabdata.service.object_std_service import (
    ObjectDefinition,
    ObjectStandardProviderService,
)
from nexuslabdata.utils import NldStrEnum


class ModelObjectNames(NldStrEnum):
    FIELD_TEMPLATE = "field_template"
    FIELD = "field"
    FIELD_ADAPTER = "field_adapter"
    FIELD_FORMAT_ADAPTER = "field_format_adapter"
    STRUCTURE_ADAPTER = "structure_adapter"
    SQL_TEMPLATE = "sql_template"
    SQL_RENDERER = "sql_renderer"


class ModelObjects:
    FIELD = ObjectDefinition(
        name=ModelObjectNames.FIELD.value,
        data_class=Field,
        folder_name="field",
    )
    FIELD_TEMPLATE = ObjectDefinition(
        name=ModelObjectNames.FIELD_TEMPLATE.value,
        data_class=FieldTemplate,
        folder_name="field_template",
    )
    FIELD_ADAPTER = ObjectDefinition(
        name=ModelObjectNames.FIELD_ADAPTER.value,
        data_class=FieldAdapter,
        folder_name="field_adapter",
    )
    FIELD_FORMAT_ADAPTER = ObjectDefinition(
        name=ModelObjectNames.FIELD_FORMAT_ADAPTER.value,
        data_class=FieldFormatAdapter,
        folder_name="field_format_adapter",
    )
    STRUCTURE_ADAPTER = ObjectDefinition(
        name=ModelObjectNames.STRUCTURE_ADAPTER.value,
        data_class=StructureAdapter,
        folder_name="structure_adapter",
    )
    SQL_TEMPLATE = ObjectDefinition(
        name=ModelObjectNames.SQL_TEMPLATE.value,
        data_class=SQLTemplateWrapper,
        folder_name="sql_template",
        file_format="jinja",
    )
    SQL_RENDERER = ObjectDefinition(
        name=ModelObjectNames.SQL_RENDERER.value,
        data_class=SQLRendererWrapper,
        folder_name="sql_renderer",
    )


MODEL_OBJECTS = [
    ModelObjects.FIELD,
    ModelObjects.FIELD_TEMPLATE,
    ModelObjects.FIELD_ADAPTER,
    ModelObjects.FIELD_FORMAT_ADAPTER,
    ModelObjects.STRUCTURE_ADAPTER,
    ModelObjects.SQL_TEMPLATE,
    ModelObjects.SQL_RENDERER,
]


class ModelService(ObjectStandardProviderService):
    def __init__(self) -> None:
        super().__init__(object_definitions=MODEL_OBJECTS)
