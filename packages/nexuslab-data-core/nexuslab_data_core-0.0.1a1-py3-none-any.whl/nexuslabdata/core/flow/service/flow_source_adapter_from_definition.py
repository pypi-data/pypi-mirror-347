from typing import Dict

from nexuslabdata.core import Structure
from nexuslabdata.core.flow.base import FlowTransformation
from nexuslabdata.core.flow.base.tfm.transformation_model import (
    FLOW_SOURCE_MODEL,
)
from nexuslabdata.core.flow.definition import FlowSourceDefinition
from nexuslabdata.core.flow.exceptions import (
    FlowAdaptationFromDefinitionException,
)
from nexuslabdata.utils.mixin import NldMixIn


class FlowSourceDefinitionAdapter(NldMixIn):
    @classmethod
    def adapt_from_definition(
        cls,
        source_definition: FlowSourceDefinition,
        source_structures: Dict[str, Structure],
    ) -> FlowTransformation:
        if source_definition is None:
            raise FlowAdaptationFromDefinitionException(
                "Source Adaptation requires a non empty source definition"
            )
        if source_definition.name not in list(source_structures.keys()):
            raise FlowAdaptationFromDefinitionException(
                f"Source Adaptation cannot be performed. The source structure {source_definition.name} "
                f"is missing from the structures provided."
            )

        return FlowTransformation(
            name=source_definition.name,
            structure=source_structures[source_definition.name],
            model=FLOW_SOURCE_MODEL,
        )
