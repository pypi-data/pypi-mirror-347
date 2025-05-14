from nexuslabdata.config.data_product import DataProduct
from nexuslabdata.service.object_std_service import (
    ObjectDefinition,
    ObjectStandardProviderService,
)
from nexuslabdata.utils import NldStrEnum


class ConfigObjectNames(NldStrEnum):
    DATA_PRODUCT = "data_product"


class ConfigObjects:
    DATA_PRODUCT = ObjectDefinition(
        name=ConfigObjectNames.DATA_PRODUCT.value,
        data_class=DataProduct,
        folder_name=ConfigObjectNames.DATA_PRODUCT.value,
    )


CONFIG_OBJECTS = [
    ConfigObjects.DATA_PRODUCT,
]


class ConfigService(ObjectStandardProviderService):
    def __init__(self) -> None:
        super().__init__(object_definitions=CONFIG_OBJECTS)
