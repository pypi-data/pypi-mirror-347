from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, cast

from nexuslabdata.core.events import CreatedStructureUsingAdaptation
from nexuslabdata.core.field import Field
from nexuslabdata.core.field.field_adapter import (
    FieldAdapter,
    FieldNamingMapping,
)
from nexuslabdata.core.field.field_template import (
    FieldTemplate,
    FieldTemplateRelativePosition,
)
from nexuslabdata.core.structure.structure import Structure
from nexuslabdata.core.structure.structure_characterisation_adapter import (
    StructureCharacterisationAdapter,
)
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn
from nexuslabdata.utils.jinja_utils import (
    render_template,
    render_template_with_none_return_allowed,
)


@dataclass
class StructureAdapter(NldNamedDataClassMixIn):
    """
    Structure Adapter

    This adapter provides a standard way to create new structure applying the adapter rules on the original structure.

    """

    field_adapter: FieldAdapter
    name_rule: str = "{{ original_structure.name }}"
    desc_rule: str = "{{ original_structure.desc }}"
    type_rule: str = "BASE TABLE"
    mandatory_parameters: List[str] = field(default_factory=list)
    field_templates: List[FieldTemplate] = field(default_factory=list)
    exclude_fields_wo_naming_mapping: bool = False
    options_to_copy: Optional[List[str]] = None
    structure_characterisation_definitions_to_keep: Optional[List[str]] = None

    def __post_init__(self) -> None:
        self._init_logger()

    def adapt_structure(self, **kwargs: Any) -> Structure:
        """
        Creates a structure based on this template

        Parameters (standard)
        -----------
            original_structure : the original structure
            field_naming_mapping : the field naming mapping (when standard mappings to apply)
            field_catalog : a dictionary of all the standard fields known, if a field is to be generated
                with a target field name available in this catalog, the field definition from the catalog
                should be used to create the new field

        Returns
        -----------
            The new structure
        """
        for parameter_name in self.mandatory_parameters:
            if parameter_name not in kwargs.keys():
                raise ValueError(
                    "Parameter "
                    + parameter_name
                    + " is mandatory for creating structure with template : "
                    + self.name
                )

        original_structure: Structure = (
            kwargs["original_structure"]
            if "original_structure" in kwargs.keys()
            else None
        )
        field_naming_mapping: FieldNamingMapping = (
            kwargs["field_naming_mapping"]
            if "field_naming_mapping" in kwargs.keys()
            else FieldNamingMapping()
        )
        field_catalog: Dict[str, Field] = (
            kwargs["field_catalog"] if "field_catalog" in kwargs.keys() else {}
        )

        creation_param_dict = {"original_structure": original_structure}

        new_structure = Structure(
            name=render_template(self.name_rule, **creation_param_dict),
            desc=render_template_with_none_return_allowed(
                self.desc_rule, **creation_param_dict
            ),
            type=render_template(self.type_rule, **creation_param_dict),
            row_count=0,
            options={
                k: v
                for k, v in original_structure.get_options().items()
                if original_structure is not None
                if k in self.options_to_copy
            }
            if self.options_to_copy is not None
            else {},
            fields=[],
        )

        target_from_source_field_naming_mapping_dict = {}
        for field in original_structure.fields:
            if self.field_adapter.should_field_be_adapted(field):
                if (not self.exclude_fields_wo_naming_mapping) | (
                    field.name in field_naming_mapping.get_fields_mapped()
                ):
                    new_field = self.field_adapter.adapt_field(
                        original_field=field,
                        field_naming_mapping=field_naming_mapping,
                        field_catalog=field_catalog,
                    )
                    target_from_source_field_naming_mapping_dict.update(
                        {new_field.name: field.name}
                    )
                    new_structure.add_field(new_field)

        self._update_structure_from_template_fields(new_structure)

        if self.structure_characterisation_definitions_to_keep:
            for (
                characterisation_definition_name
            ) in self.structure_characterisation_definitions_to_keep:
                for (
                    characterisation
                ) in original_structure.get_characterisations_with_definition_name(
                    characterisation_definition_name
                ):
                    new_characterisation = StructureCharacterisationAdapter.adapt_structure_characterisation(
                        characterisation,
                        target_from_source_field_naming_mapping_dict,
                        new_structure.name,
                    )
                    new_structure.add_characterisation(new_characterisation)

        self.log_event(
            CreatedStructureUsingAdaptation(
                structure_name=new_structure.name,
                adapter_name=self.name,
                original_structure_name=original_structure.name,
            )
        )
        return new_structure

    # Field Template methods
    def get_field_templates_with_existing_override_on_characterisation(
        self,
    ) -> List[FieldTemplate]:
        return [
            field_template
            for field_template in self.field_templates
            if field_template.override_existing_field_on_characterisation
            is not None
        ]

    def get_field_templates_at_start(self) -> List[FieldTemplate]:
        return [
            field_rule
            for field_rule in self.field_templates
            if field_rule.relative_position
            == FieldTemplateRelativePosition.START
        ]

    def get_field_templates_at_end(self) -> List[FieldTemplate]:
        return [
            field_rule
            for field_rule in self.field_templates
            if field_rule.relative_position == FieldTemplateRelativePosition.END
        ]

    def _update_structure_from_template_fields(
        self, structure: Structure
    ) -> None:
        """
        Updates a structure using template field rules

        Parameters
        -----------
            structure : the Data Structure to update
        """
        if self.field_templates is not None:
            """Remove existing field when override required"""
            for (
                field_template
            ) in (
                self.get_field_templates_with_existing_override_on_characterisation()
            ):
                for (
                    field_to_remove
                ) in structure.get_fields_with_characterisation_name(
                    cast(
                        str,
                        field_template.override_existing_field_on_characterisation,
                    )
                ):
                    structure.remove_field(field_to_remove.name)

            """ Add standard field templates """
            i = 1
            for field_template in self.get_field_templates_at_start():
                field_to_add = field_template.get_field_instance()
                field_to_add.position = i
                structure.add_field(new_field=field_to_add, force_position=True)
                i += 1

            for field_template in self.get_field_templates_at_end():
                structure.add_field(
                    new_field=field_template.get_field_instance(),
                    force_position=False,
                )

        structure.sort_fields_by_ordinal_position()
