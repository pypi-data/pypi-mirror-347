from dataclasses import dataclass, field
from typing import Dict, List, Optional

from nexuslabdata.core import Structure
from nexuslabdata.core.flow.base.field.field_group import (
    FlowTransformationFieldGroup,
    FlowTransformationFieldGroupType,
    StdFlowTransformationFieldGroupNames,
)
from nexuslabdata.core.flow.base.tfm.transformation_model import (
    FlowTransformationModel,
    StdFlowTransformationModelNames,
)
from nexuslabdata.core.flow.exceptions import FlowException
from nexuslabdata.utils.data_class_mixin import NldDataClassMixIn


@dataclass
class FlowTransformation(NldDataClassMixIn):
    name: str
    model: FlowTransformationModel
    structure: Optional[Structure] = None
    attributes: Optional[Dict[str, str]] = None
    field_groups: Dict[str, List[FlowTransformationFieldGroup]] = field(
        default_factory=dict
    )
    predecessors: Optional[List[str]] = None

    def __post_init__(self) -> None:
        # Initialization of all the field groups
        self._init_field_groups()

        # Initialization of the structures for transformation and field group levels
        if self.model.tfm_standard_structure:
            if self.structure is None:
                raise FlowException(
                    f"Flow Transformation with model {self.model.name} has standard structure but no structure was provided."
                )
            self.update_tfm_structure(self.structure)

    # Transformation methods
    def is_source(self) -> bool:
        return self.model.name == StdFlowTransformationModelNames.SOURCE

    def is_target(self) -> bool:
        return self.model.name == StdFlowTransformationModelNames.TARGET

    # Field Group methods
    def _init_field_groups(self) -> None:
        """
        Initializes all the default field groups in the transformation.
        Uses the Transformation Model of this transformation to initialize all the field groups.

        Once field groups are initialized, the field group structures are updated if provided as parameter

        """
        self.field_groups = {
            FlowTransformationFieldGroupType.INPUT: [],
            FlowTransformationFieldGroupType.OUTPUT: [],
        }
        for field_group_model in self.model.field_group_models:
            self.add_field_group(
                field_group_model.type,
                FlowTransformationFieldGroup(
                    name=StdFlowTransformationFieldGroupNames.DEFAULT,
                    model=field_group_model,
                ),
            )

    def get_field_groups_as_dict(
        self,
    ) -> Dict[str, List[FlowTransformationFieldGroup]]:
        return self.field_groups if self.field_groups is not None else {}

    def get_field_groups_by_type(
        self,
    ) -> Dict[str, List[FlowTransformationFieldGroup]]:
        return self.field_groups if self.field_groups is not None else {}

    def get_field_groups(
        self, fld_group_type: Optional[str] = None, name: Optional[str] = None
    ) -> List[FlowTransformationFieldGroup]:
        """
        Get the field group based on nothing or type and/or name

        Parameters
        -----------
            fld_group_type : the field group type (can be INPUT, VARIABLE, OUTPUT or IN_OUT)
            name : the field group type name

        Returns
        -----------
            The list of field groups of the provided type and with the provided name.
            If no field group matches these criteria, an empty list is returned
        """
        if fld_group_type is not None:
            if name is not None:
                return [
                    self.get_field_group(
                        fld_group_type=fld_group_type, name=name
                    )
                ]
            else:
                return self.field_groups[fld_group_type]
        else:
            return self.get_all_field_groups_as_list()

    def get_single_field_group(
        self, fld_group_type: str
    ) -> FlowTransformationFieldGroup:
        # TODO : Validate this method
        if (
            fld_group_type in self.get_field_groups_as_dict()
            and len(self.get_field_groups_as_dict()[fld_group_type]) > 0
        ):
            raise FlowException(
                f"No field group of type {fld_group_type} available in tranformation : {self.name}"
            )
        return self.get_field_groups_as_dict()[fld_group_type]  # type: ignore

    def get_single_input_field_group(self) -> FlowTransformationFieldGroup:
        return self.get_single_field_group(
            FlowTransformationFieldGroupType.INPUT
        )

    def get_single_output_field_group(self) -> FlowTransformationFieldGroup:
        return self.get_single_field_group(
            FlowTransformationFieldGroupType.OUTPUT
        )

    def get_field_group(
        self, fld_group_type: str, name: str
    ) -> FlowTransformationFieldGroup:
        """
        Get a field group based on its type and its name

        Parameters
        -----------
            fld_group_type : the field group type (can be INPUT, VARIABLE, OUTPUT)
            name : the field group type name

        Returns
        -----------
            The field group of the provided type and with the provided name.
            If no field group matches these criterias, an exception is thrown
        """
        for fld_group in self.get_field_groups_as_dict()[fld_group_type]:
            if fld_group.name == name:
                return fld_group
        raise FlowException(
            f"No Field Group with type {fld_group_type} and name {name} is available in the transformation {self.name}"
        )

    def add_field_group(
        self,
        fld_group_type: str,
        field_group: FlowTransformationFieldGroup,
    ) -> None:
        """
        Add a field group to this transformation
        A check is being done to check that the field group name is not already used.

        Parameters
        -----------
            fld_group_type : the field group type (can be INPUT, VARIABLE, OUTPUT)
            field_group : the field_group to add
        """
        if fld_group_type not in [
            FlowTransformationFieldGroupType.INPUT,
            FlowTransformationFieldGroupType.OUTPUT,
        ]:
            raise ValueError(
                "Field Group Type : " + fld_group_type + " is not allowed."
            )
        if field_group is None:
            raise ValueError("Cannot add an empty field_group")
        if self.get_field_group(fld_group_type, field_group.name) is not None:
            raise ValueError(
                "Field Group for type : "
                + fld_group_type
                + " already exists with name : "
                + field_group.name
            )
        self.field_groups[fld_group_type].append(field_group)

    def get_input_field_groups(self) -> List[FlowTransformationFieldGroup]:
        return self.get_field_groups(
            fld_group_type=FlowTransformationFieldGroupType.INPUT
        )

    def get_output_field_groups(self) -> List[FlowTransformationFieldGroup]:
        return self.get_field_groups(
            fld_group_type=FlowTransformationFieldGroupType.OUTPUT
        )

    def update_field_group_structure(
        self, fld_group_type: str, fld_group_name: str, structure: Structure
    ) -> None:
        """
        Update an available field group with a specific structure

        Parameters
        -----------
            fld_group_type : the field group type (can be INPUT, VARIABLE, OUTPUT or IN_OUT)
            fld_group_name : the field group name
            structure : the structure to apply to the field group
        """
        fld_group: FlowTransformationFieldGroup = self.get_field_group(
            fld_group_type, fld_group_name
        )
        if fld_group is not None:
            fld_group.update_data_structure(structure=structure)

    def get_all_field_groups_as_list(
        self,
    ) -> List[FlowTransformationFieldGroup]:
        """
        Get all the field groups

        Returns
        -----------
            The list of field groups
        """
        fld_groups = []
        fld_groups.extend(
            self.get_field_groups(
                fld_group_type=FlowTransformationFieldGroupType.INPUT
            )
        )
        fld_groups.extend(
            self.get_field_groups(
                fld_group_type=FlowTransformationFieldGroupType.OUTPUT
            )
        )
        return fld_groups

    # Standard structure methods
    def update_tfm_structure(self, tfm_structure: Structure) -> None:
        """
        Update the standard transformation structure.

        A check is done to verify the model allows standard transformation

        Parameters
        -----------
            tfm_structure : the structure to apply to this transformation
        """
        if tfm_structure is None:
            self.structure = tfm_structure
            return
        if not self.model.tfm_standard_structure:
            raise ValueError(
                "A standard structure is provided but model : "
                + self.model.name
                + " does not allow standard structure"
            )
        else:
            self.structure = tfm_structure

        for fld_group in self.get_all_field_groups_as_list():
            fld_group.update_data_structure(Structure.deep_copy(tfm_structure))
