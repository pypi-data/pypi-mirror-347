import dataclasses
from typing import Dict, List, Optional

from nexuslabdata.core.field.field import Field
from nexuslabdata.core.field.field_characterisation import FieldCharacterisation
from nexuslabdata.core.field.field_characterisation_def import (
    FieldCharacterisationDefinitionNames,
    FieldCharacterisationDefinitions,
)
from nexuslabdata.core.field.field_format_adapter import FieldFormatAdapter
from nexuslabdata.utils.data_class_mixin import (
    NldDataClassMixIn,
    NldNamedDataClassMixIn,
)
from nexuslabdata.utils.jinja_utils import (
    render_template,
    render_template_with_none_return_allowed,
)


@dataclasses.dataclass
class FieldNamingMapping(NldDataClassMixIn):
    """
    Example of field naming mapping dictionary :
        {
            'prefix' : 'PREFIX_VALUE'
            , 'suffix' : 'SUFFIX_VALUE'
            , 'rules' :
                {
                'name' : {'override_name' : 'PDT_CAT_LV0'}
                , 'sdesc1' : {'override_name' : 'PDT_CAT_LV0_SHT_FRE_DSC'}
                , 'sdesc2' : {'override_name' : 'PDT_CAT_LV0_SHT_ENG_DSC'}
                , 'ldesc1' : {'override_name' : 'PDT_CAT_LV0_LNG_FRE_DSC'}
                , 'ldesc2' : {'override_name' : 'PDT_CAT_LV0_LNG_ENG_DSC'}
                }
        }
    """

    prefix: str = ""
    suffix: str = ""
    rules: Dict[str, Dict[str, str]] = dataclasses.field(default_factory=dict)

    def get_fields_mapped(self) -> List[str]:
        return list(self.rules.keys())

    def has_specific_naming_rule(self, name: str) -> bool:
        """
        Checks if the provided field name has a specific naming rule

        Parameters
        -----------
            name : the field name to check

        Returns
        -----------
            True if the field name has a specific naming rule, False otherwise
        """
        field_naming_rule = self.get_field_naming_rule(name)
        if field_naming_rule is None:
            return False
        return "rule" in field_naming_rule.keys()

    def get_field_naming_rule(self, name: str) -> Optional[Dict[str, str]]:
        """
        Get the field naming rule for a specific field name

        Parameters
        -----------
            name : the field name

        Returns
        -----------
            The field naming rule for the provided field name (the target naming of the field)
        """
        if name in list(self.rules.keys()):
            return self.rules[name]
        return None

    def get_target_field_name(self, name: str) -> str:
        """
        Get the target field name for an input field name

        Parameters
        -----------
            name : the field name

        Returns
        -----------
            The target field name for this field naming rules
        """
        fld_specific_naming_rule = self.get_field_naming_rule(name)
        if fld_specific_naming_rule is None:
            return name
        if "override_name" in fld_specific_naming_rule.keys():
            return fld_specific_naming_rule["override_name"]
        rule = fld_specific_naming_rule["rule"]
        rule_params = {
            "field_general_prefix": self.prefix,
            "field_general_suffix": self.suffix,
            "prefix": fld_specific_naming_rule["prefix"]
            if "prefix" in fld_specific_naming_rule.keys()
            else "",
            "suffix": fld_specific_naming_rule["suffix"]
            if "suffix" in fld_specific_naming_rule.keys()
            else "",
        }
        return render_template(rule, **rule_params)


@dataclasses.dataclass
class FieldAdapter(NldNamedDataClassMixIn):
    name_rule: str = "{{ original_field.name }}"
    desc_rule: str = "{{ original_field.desc }}"
    all_fields_optional: bool = False
    # keep_tec_key: bool = True # TODO: Change this code for structure characterisation
    # keep_func_key: bool = True # TODO: Change this code for structure characterisation
    orig_to_new_characterisation_mapping: Optional[Dict[str, str]] = None
    field_format_adapter: Optional[FieldFormatAdapter] = None
    field_names_to_exclude: Optional[List[str]] = None
    field_data_types_to_exclude: Optional[List[str]] = None
    field_characterisations_to_exclude: Optional[List[str]] = None
    exclude_fields_without_characterisations: bool = False

    def adapt_field(
        self,
        original_field: Field,
        field_naming_mapping: FieldNamingMapping = FieldNamingMapping(),
        field_catalog: Dict[str, Field] = {},
    ) -> Field:
        if field_naming_mapping.has_specific_naming_rule(original_field.name):
            # Whenever a specific naming rule is provided, this rules is of higher priority
            return self.create_new_field(
                original_field,
                override_params={
                    "field_name": field_naming_mapping.get_target_field_name(
                        original_field.name
                    )
                },
            )
        else:
            field_name_override = field_naming_mapping.get_target_field_name(
                original_field.name
            )
            if field_name_override in field_catalog.keys():
                # This means the field has a default definition to be considered
                return self.create_new_field(field_catalog[field_name_override])
            else:
                return self.create_new_field(
                    original_field,
                    override_params={
                        "field_name": field_naming_mapping.get_target_field_name(
                            original_field.name
                        )
                    },
                )

    def get_orig_to_new_characterisation_mapping(self) -> Dict[str, str]:
        return (
            self.orig_to_new_characterisation_mapping
            if self.orig_to_new_characterisation_mapping is not None
            else {}
        )

    def get_field_names_to_exclude(self) -> List[str]:
        return (
            self.field_names_to_exclude
            if self.field_names_to_exclude is not None
            else []
        )

    def get_field_data_types_to_exclude(self) -> List[str]:
        return (
            self.field_data_types_to_exclude
            if self.field_data_types_to_exclude is not None
            else []
        )

    def get_field_characterisations_to_exclude(self) -> List[str]:
        return (
            self.field_characterisations_to_exclude
            if self.field_characterisations_to_exclude is not None
            else []
        )

    def should_field_be_adapted(self, field: Field) -> bool:
        if (
            (field.name not in self.get_field_names_to_exclude())
            & (field.data_type not in self.get_field_data_types_to_exclude())
            & (
                len(
                    [
                        characterisation.name
                        for characterisation in field.get_characterisations()
                        if characterisation.name
                        in self.get_field_characterisations_to_exclude()
                    ]
                )
                == 0
            )
            & (
                (not self.exclude_fields_without_characterisations)
                | (field.has_characterisations())
            )
        ):
            return True
        return False

    def create_new_field(
        self, original_field: Field, override_params: Dict[str, str] = {}
    ) -> Field:
        """
        Creates a field based on this template

        Parameters
        -----------
            original_field : the original field
            override_params : the override parameters (allowed override parameters are "field_name")

        Returns
        -----------
            The new field
        """
        new_characterisations = []
        if original_field.characterisations is not None:
            for characterisation in original_field.characterisations:
                if (
                    characterisation.name
                    == FieldCharacterisationDefinitionNames.MANDATORY
                ):
                    if not self.all_fields_optional:
                        new_characterisations.append(
                            FieldCharacterisation.create_from_definition(
                                FieldCharacterisationDefinitions.MANDATORY
                            )
                        )
                # TODO : Update the code
                # Technical and functional key characterisation code removed
                elif characterisation.name in list(
                    self.get_orig_to_new_characterisation_mapping().keys()
                ):
                    tgt_characterisation_name = (
                        self.get_orig_to_new_characterisation_mapping()[
                            characterisation.name
                        ]
                    )
                    new_characterisations.append(
                        FieldCharacterisation(tgt_characterisation_name, None)
                    )
                else:
                    new_characterisations.append(characterisation)

        new_field_format = (
            self.field_format_adapter.get_adapted_field_format(
                data_type=original_field.data_type,
                length=original_field.length,
                precision=original_field.precision,
                characterisations=original_field.get_characterisation_names(),
            )
            if self.field_format_adapter is not None
            else (
                original_field.data_type,
                original_field.length,
                original_field.precision,
            )
        )

        creation_param_dict = {}
        creation_param_dict["original_field"] = original_field.as_dict()
        creation_param_dict["override_params"] = (
            override_params if override_params is not None else {}
        )

        return Field(
            name=render_template(self.name_rule, **creation_param_dict),
            desc=render_template_with_none_return_allowed(
                self.desc_rule, **creation_param_dict
            ),
            position=0,
            data_type=new_field_format[0],
            length=new_field_format[1],
            precision=new_field_format[2],
            default_value=original_field.default_value,
            characterisations=new_characterisations,
        )
