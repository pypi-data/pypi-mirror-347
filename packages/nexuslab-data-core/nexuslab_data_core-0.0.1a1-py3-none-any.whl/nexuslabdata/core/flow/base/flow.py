from dataclasses import dataclass
from typing import List, Optional

from nexuslabdata.core.flow.base.field.field_group import (
    FlowTransformationFieldGroup,
    FlowTransformationFieldGroupType,
)
from nexuslabdata.core.flow.base.tfm import (
    FlowTransformation,
    FlowTransformationLink,
)
from nexuslabdata.core.flow.exceptions import (
    FlowException,
    NoTransformationLinkFoundException,
)
from nexuslabdata.core.flow.incremental import FLOW_INCREMENTAL_TYPE_LITERAL
from nexuslabdata.core.flow.utils import FLOW_UPDATE_STRATEGY_LITERAL
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class Flow(NldDataClassMixIn):
    name: str
    update_strategy: FLOW_UPDATE_STRATEGY_LITERAL
    incremental_type: FLOW_INCREMENTAL_TYPE_LITERAL
    sources: List[FlowTransformation]
    target: FlowTransformation
    transformations: Optional[List[FlowTransformation]] = None
    transformation_links: Optional[List[FlowTransformationLink]] = None

    # Transformation methods
    def get_transformations(self) -> List[FlowTransformation]:
        return self.transformations if self.transformations is not None else []

    def get_transformation(self, name: str) -> FlowTransformation:
        tfms = [tfm for tfm in self.get_transformations() if tfm.name == name]
        if len(tfms) == 0:
            raise FlowException(
                f"The transformation {name} does not exist inside the flow : {name}"
            )
        if len(tfms) > 1:
            raise FlowException(
                f"The transformation {name} is available {len(tfms)} inside the flow : {name}"
            )
        return tfms[0]

    def get_all_source_tfms(self) -> List[FlowTransformation]:
        return [tfm for tfm in self.get_transformations() if tfm.is_source()]

    def get_all_target_tfms(self) -> List[FlowTransformation]:
        return [tfm for tfm in self.get_transformations() if tfm.is_target()]

    # Transformation link methods
    def get_transformation_links(self) -> List[FlowTransformationLink]:
        return (
            self.transformation_links
            if self.transformation_links is not None
            else []
        )

    def _add_transformation_link(
        self,
        src_tfm: str,
        src_fld_grp: str,
        tgt_tfm: str,
        tgt_fld_grp: str,
        propagate_structure_forward: bool = False,
        propagate_structure_backward: bool = False,
    ) -> None:
        src_fld_group: FlowTransformationFieldGroup = self.get_field_group(
            tfm_name=src_tfm,
            fld_grp_type=FlowTransformationFieldGroupType.OUTPUT,
            fld_grp_name=src_fld_grp,
        )
        tgt_fld_group: FlowTransformationFieldGroup = self.get_field_group(
            tfm_name=tgt_tfm,
            fld_grp_type=FlowTransformationFieldGroupType.INPUT,
            fld_grp_name=tgt_fld_grp,
        )
        if src_fld_group is None:
            raise ValueError(
                "Source Field Group : "
                + src_fld_grp
                + " in transformation : "
                + src_tfm
                + " does not exist"
            )
        if tgt_fld_group is None:
            raise ValueError(
                "Target Field Group : "
                + tgt_fld_grp
                + " in transformation : "
                + tgt_tfm
                + " does not exist"
            )
        existing_tfm_link = self.get_transformation_link(
            src_tfm, src_fld_grp, tgt_tfm, tgt_fld_grp
        )
        if existing_tfm_link is not None:
            raise ValueError(
                "Data Flow link already exists between "
                + src_tfm
                + "/"
                + src_fld_grp
                + " and "
                + tgt_tfm
                + "/"
                + tgt_fld_grp
            )

        new_data_flow_link = FlowTransformationLink(
            source_tfm=src_tfm,
            source_fld_group=src_fld_grp,
            target_tfm=tgt_tfm,
            target_fld_group=tgt_fld_grp,
            automatic_linkage=True,
        )
        self.transformation_links.append(new_data_flow_link)

        if propagate_structure_forward & (src_fld_group.structure is not None):
            # Propagate the structure from the source of the link to the target field group
            tfm = self.get_transformation(name=tgt_tfm)
            new_structure = src_fld_group.structure.deep_copy()
            if tfm.model.tfm_standard_structure:
                tfm.update_tfm_structure(new_structure)
            else:
                tgt_fld_group.update_data_structure(new_structure)

        if propagate_structure_backward & (tgt_fld_group.structure is not None):
            # Propagate the structure from the target of the link to the source field group
            tfm = self.get_transformation(name=src_tfm)
            new_structure = tgt_fld_group.structure.deep_copy()
            if tfm.model.tfm_standard_structure:
                tfm.update_tfm_structure(new_structure)
            else:
                src_fld_group.update_data_structure(new_structure)

    def get_transformation_link(
        self,
        src_tfm: Optional[str] = None,
        src_fld_grp: Optional[str] = None,
        tgt_tfm: Optional[str] = None,
        tgt_fld_grp: Optional[str] = None,
    ) -> FlowTransformationLink:
        """
        Get a flow link based on the source and target information

        Parameters
        -----------
            src_tfm : the name of the source transformation
            src_fld_grp : the name of the source field group
            tgt_tfm : the name of the target transformation
            tgt_fld_grp : the name of the target field group

        Returns
        -----------
            The flow link if it is found
        """
        if (src_tfm is not None) & (src_fld_grp is not None):
            if (tgt_tfm is not None) & (tgt_fld_grp is not None):
                for tfm_link in self.get_transformation_links():
                    if (
                        (tfm_link.source_tfm == src_tfm)
                        & (tfm_link.source_fld_group == src_fld_grp)
                        & (tfm_link.target_tfm == tgt_tfm)
                        & (tfm_link.target_fld_group == tgt_fld_grp)
                    ):
                        return tfm_link
            else:
                for tfm_link in self.get_transformation_links():
                    if (tfm_link.source_tfm == src_tfm) & (
                        tfm_link.source_fld_group == src_fld_grp
                    ):
                        return tfm_link
        else:
            if (tgt_tfm is not None) & (tgt_fld_grp is not None):
                for tfm_link in self.get_transformation_links():
                    if (tfm_link.target_tfm == tgt_tfm) & (
                        tfm_link.target_fld_group == tgt_fld_grp
                    ):
                        return tfm_link
        raise NoTransformationLinkFoundException(
            flow_name=self.name,
            src_tfm=src_tfm,
            src_fld_grp=src_fld_grp,
            tgt_tfm=tgt_tfm,
            tgt_fld_grp=tgt_fld_grp,
        )

    def get_transformation_links_based_on_tfm_names(
        self, src_tfm: Optional[str] = None, tgt_tfm: Optional[str] = None
    ) -> List[FlowTransformationLink]:
        tfm_links: List[FlowTransformationLink] = []
        if (src_tfm is not None) & (tgt_tfm is not None):
            for tfm_link in self.get_transformation_links():
                if (tfm_link.source_tfm == src_tfm) & (
                    tfm_link.target_tfm == tgt_tfm
                ):
                    tfm_links.append(tfm_link)
        elif src_tfm is not None:
            for tfm_link in self.get_transformation_links():
                if tfm_link.source_tfm == src_tfm:
                    tfm_links.append(tfm_link)
        elif tgt_tfm is not None:
            for tfm_link in self.get_transformation_links():
                if tfm_link.target_tfm == tgt_tfm:
                    tfm_links.append(tfm_link)
        else:
            tfm_links = self.get_transformation_links()
        return tfm_links

    # Field Group methods
    def get_input_field_groups(
        self, tfm_name: str
    ) -> List[FlowTransformationFieldGroup]:
        return self.get_transformation(tfm_name).get_input_field_groups()

    def get_output_field_groups(
        self, tfm_name: str
    ) -> List[FlowTransformationFieldGroup]:
        return self.get_transformation(tfm_name).get_output_field_groups()

    def get_field_group(
        self, tfm_name: str, fld_grp_type: str, fld_grp_name: str
    ) -> FlowTransformationFieldGroup:
        """
        Get a specific field group inside a transformation based on the transformation name, field group type and field group name.
        All these parameters are mandatory

        Parameters
        -----------
            tfm_name : the name of the transformation to look for in this data flow
            fld_grp_type : the field group type
            fld_grp_name : the field group name

        Returns
        -----------
            The field group if it is found
        """
        return self.get_transformation(tfm_name).get_field_group(
            fld_group_type=fld_grp_type, name=fld_grp_name
        )
