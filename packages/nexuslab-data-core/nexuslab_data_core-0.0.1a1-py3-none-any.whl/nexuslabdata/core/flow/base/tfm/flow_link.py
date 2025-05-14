from dataclasses import dataclass

from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FlowTransformationLink(NldDataClassMixIn):
    source_tfm: str
    source_fld_group: str
    target_tfm: str
    target_fld_group: str
    automatic_linkage: bool = True
