from typing import Dict, List

from nexuslabdata.core import Structure
from nexuslabdata.core.flow import FlowDefinition
from nexuslabdata.core.flow.base import (
    Flow,
    FlowTransformation,
    FlowTransformationLink,
)
from nexuslabdata.core.flow.base.field.field_group import (
    StdFlowTransformationFieldGroupNames,
)
from nexuslabdata.core.flow.definition import FlowTransformationDefinition
from nexuslabdata.core.flow.service.flow_source_adapter_from_definition import (
    FlowSourceDefinitionAdapter,
)
from nexuslabdata.core.flow.service.flow_transformation_adapter_from_definition import (
    FlowTransformationDefinitionAdapter,
)
from nexuslabdata.utils.mixin import NldMixIn


class FlowDefinitionAdapter(NldMixIn):
    @classmethod
    def adapt_from_definition(
        cls,
        flow_definition: FlowDefinition,
        source_structures: Dict[str, Structure],
    ) -> Flow:
        """
        Adaptation is done with the following steps :
        1. Create the flow sources based on the definition and the source structures
        2. Create one by one each transformation from the sources to the target
        3. Create the target linked directly to the last transformation of the DAG

        :param flow_definition: the flow definition
        :param source_structures: the source structures of the flow definition
        :return: a new flow
        """

        flow_sources: List[FlowTransformation] = []
        for source_definition in flow_definition.sources:
            flow_sources.append(
                FlowSourceDefinitionAdapter.adapt_from_definition(
                    source_definition, source_structures=source_structures
                )
            )
        flow_transformations: List[FlowTransformation] = []
        flow_transformation_links: List[FlowTransformationLink] = []
        flow_definition_graph = flow_definition.get_flow_definition_graph()
        tfm_and_target_nodes = (
            flow_definition_graph.get_graph_nodes_as_list_using_bfs_from_source()
        )
        for node in tfm_and_target_nodes:
            current_node = flow_definition_graph.graph.nodes[node]
            if isinstance(current_node.tfm, FlowTransformationDefinition):
                predecessors = flow_definition_graph.get_direct_predecessors(
                    current_node
                )
                predecessor_structures: Dict[str, Structure] = {}
                for predecessor in predecessors:
                    for source in flow_sources:
                        if source.name == predecessor:
                            structure = (
                                source.get_single_output_field_group().structure
                            )
                            if structure is not None:
                                predecessor_structures.update(
                                    {source.name: structure}
                                )

                    for transformation in flow_transformations:
                        if transformation.name == predecessor:
                            structure = (
                                source.get_single_output_field_group().structure
                            )
                            if structure is not None:
                                predecessor_structures.update(
                                    {source.name: structure}
                                )
                    flow_transformation_links.append(
                        FlowTransformationLink(
                            source_tfm=predecessor,
                            source_fld_group=StdFlowTransformationFieldGroupNames.DEFAULT,
                            target_tfm=node,
                            target_fld_group=StdFlowTransformationFieldGroupNames.DEFAULT,
                        )
                    )
                transformation = (
                    FlowTransformationDefinitionAdapter.adapt_from_definition(
                        flow_definition.get_transformation_by_name(
                            current_node
                        ),
                        predecessor_structures=predecessor_structures,
                    )
                )
                flow_transformations.append(transformation)

        # TODO : Correct target
        return Flow(
            name=flow_definition.name,
            update_strategy=flow_definition.update_strategy,
            incremental_type=flow_definition.incremental_type,
            sources=flow_sources,
            target=None,  # type: ignore
            transformations=flow_transformations,
            transformation_links=flow_transformation_links,
        )
