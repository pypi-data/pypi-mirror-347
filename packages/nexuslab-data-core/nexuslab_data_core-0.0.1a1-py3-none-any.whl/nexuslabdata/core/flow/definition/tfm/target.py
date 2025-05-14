from dataclasses import dataclass

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FlowTargetDefinition(NldDataClassMixIn):
    namespace: str
    name: str
