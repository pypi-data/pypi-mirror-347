from dataclasses import dataclass
from typing import List, Optional

import networkx as nx

from nexuslabdata.core.flow.definition.tfm import (
    FlowSourceDefinition,
    FlowTargetDefinition,
    FlowTransformationDefinition,
)
from nexuslabdata.core.flow.exceptions import FlowDefinitionException
from nexuslabdata.core.flow.incremental import FLOW_INCREMENTAL_TYPE_LITERAL
from nexuslabdata.core.flow.utils import FLOW_UPDATE_STRATEGY_LITERAL
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn
from nexuslabdata.utils.mixin import NldMixIn


@dataclass
class FlowDefinition(NldDataClassMixIn):
    name: str
    model: str
    target: FlowTargetDefinition
    sources: List[FlowSourceDefinition]
    update_strategy: FLOW_UPDATE_STRATEGY_LITERAL
    incremental_type: FLOW_INCREMENTAL_TYPE_LITERAL
    transformations: Optional[List[FlowTransformationDefinition]] = None

    def __post_init__(self) -> None:
        if len(self.sources) == 0:
            raise FlowDefinitionException(
                f"The flow {self.name} has no sources available, which is not authorized"
            )

    def get_master_source(self) -> FlowSourceDefinition:
        if len(self.sources) == 0:
            raise FlowDefinitionException(
                f"No source available in flow : {self.name}"
            )
        return self.sources[0]

    def get_flow_definition_graph(self) -> "FlowDefinitionGraph":
        return FlowDefinitionGraph(self)

    def get_transformations(self) -> List[FlowTransformationDefinition]:
        return self.transformations if self.transformations is not None else []

    def get_transformation_by_name(
        self, tfm_name: str
    ) -> FlowTransformationDefinition:
        transformations_matching_name = [
            tfm for tfm in self.get_transformations() if tfm.name == tfm_name
        ]
        if len(transformations_matching_name) == 0:
            raise FlowDefinitionException(
                f"No transformation with name {tfm_name} available in the flow definition {self.name}"
            )
        return transformations_matching_name[0]


class FlowDefinitionGraph(NldMixIn):
    def __init__(self, flow_definition: FlowDefinition) -> None:
        self.init_graph_from_data_flow(flow_definition)

    def init_graph_from_data_flow(
        self, flow_definition: FlowDefinition
    ) -> None:
        self.graph = nx.DiGraph()
        self.flow_definition = flow_definition
        for source in flow_definition.sources:
            self.graph.add_node(source.name, tfm=source)
        if flow_definition.target is not None:
            self.graph.add_node(
                flow_definition.target.name, tfm=flow_definition.target
            )
        for tfm in flow_definition.get_transformations():
            self.graph.add_node(tfm.name, tfm=tfm)

        for tfm in flow_definition.get_transformations():
            if tfm.predecessors is not None and len(tfm.predecessors) > 0:
                for predecessor in tfm.predecessors:
                    self.graph.add_edge(predecessor, tfm.name)
            else:
                # Case of the first transformation to be linked to the source (applies only when a single source is available)
                if len(flow_definition.sources) > 1:
                    raise FlowDefinitionException(
                        f"The transformation {tfm.name} has no predecessor and the flow definition contains {len(flow_definition.sources)} sources"
                    )
                self.graph.add_edge(
                    flow_definition.get_master_source().name, tfm.name
                )

        main_target_predecessors = list(
            self.graph.predecessors(flow_definition.target.name)  # type: ignore
        )
        target_tfm_to_link = (
            main_target_predecessors[len(main_target_predecessors) - 1]
            if len(main_target_predecessors) > 0
            else flow_definition.target.name
        )

        main_source_successors = list(
            nx.descendants(self.graph, flow_definition.get_master_source().name)  # type: ignore
        )
        main_source_successors_wo_output = []
        for successor in main_source_successors:
            if self.graph.out_degree(successor) == 0:
                main_source_successors_wo_output.append(successor)
        source_tfm_to_link = (
            main_source_successors_wo_output[
                len(main_source_successors_wo_output) - 1
            ]
            if len(main_source_successors_wo_output) > 0
            else flow_definition.get_master_source().name
        )

        self.graph.add_edge(source_tfm_to_link, target_tfm_to_link)

    def get_direct_predecessors(self, node: str) -> List[str]:
        return list(self.graph.predecessors(node))  # type: ignore

    def get_graph_nodes_as_list_using_bfs_from_source(self) -> List[str]:
        return list(
            nx.bfs_tree(
                self.graph, source=self.flow_definition.get_master_source().name
            ).nodes
        )[1:]
