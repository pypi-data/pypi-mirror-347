from typing import Dict

from nexuslabdata.core import Structure
from nexuslabdata.core.flow.base import FlowTransformation
from nexuslabdata.core.flow.base.tfm.transformation_model import (
    FLOW_STANDARD_MODEL,
)
from nexuslabdata.core.flow.definition import FlowTransformationDefinition
from nexuslabdata.core.flow.exceptions import (
    FlowAdaptationFromDefinitionException,
)
from nexuslabdata.utils.mixin import NldMixIn


class FlowTransformationDefinitionAdapter(NldMixIn):
    @classmethod
    def adapt_from_definition(
        cls,
        transformation_definition: FlowTransformationDefinition,
        predecessor_structures: Dict[str, Structure],
    ) -> FlowTransformation:
        if transformation_definition is None:
            raise FlowAdaptationFromDefinitionException(
                "Transformation Adaptation requires a non empty transformation definition"
            )
        transformation = FlowTransformation(
            name=transformation_definition.name,
            model=FLOW_STANDARD_MODEL,
        )

        return transformation
