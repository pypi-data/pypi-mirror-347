from typing import Any, Dict, Optional

from jinja2 import Template

from nexuslabdata.core.structure.structure import Structure
from nexuslabdata.core.structure.structure_characterisation_def import (
    StructureCharacterisationDefinitionNames,
)
from nexuslabdata.core.structure.structure_referential import StructureNamespace
from nexuslabdata.utils.datetime_util import get_current_datetime


class StructureSqlRenderer:
    """
    Structure SQL Renderer

    Provides method to convert a structure to a dictionary interpretable by jinja.
    This class can be inherited to provide a different method of dictionary interpretations
    """

    @classmethod
    def get_structure_dict_for_jinja_rendering(
        cls, structure: Structure
    ) -> dict[str, Any]:
        """
            Get a structure dictionary for jinja rendering

            Output Dictionary contains :
            - All the structure attributes and field attributes (with an additional field-level information provided for mandatory fields)
            - last_update_tst_field : The last update timestamp field, if available
            - source_last_update_tst_field : The source last update timestamp field, if available
            - insert_tst_field : The insert timestamp field, if available

        Parameters
        -----------
            structure : Structure
                A structure

        Returns
        -----------
            The structure dictionary for jinja rendering
        """
        structure_dict = structure.as_dict()

        # Primary Key specific rule
        pk_characterisation = (
            structure.get_characterisation_with_definition_name(
                StructureCharacterisationDefinitionNames.PRIMARY_KEY
            )
        )
        if pk_characterisation is not None:
            structure_dict["primary_key"] = pk_characterisation.as_dict()

        structure_dict[
            "last_update_tst_field"
        ] = structure.get_last_update_tst_field()
        structure_dict[
            "source_last_update_tst_field"
        ] = structure.get_source_last_update_tst_field()
        structure_dict["insert_tst_field"] = structure.get_insert_tst_field()
        return structure_dict

    @classmethod
    def get_generic_param_dict(cls) -> Dict[str, str]:
        """
        Get the generic parameter dictionary.

        Output Dictionary contains :
            - cur_date_str : the current date formatted as %d-%m-Y

        Returns
        -------
            A dictionary, which all generic parameters (not specific to the input information)
        """
        return {"cur_date_str": get_current_datetime().strftime("%d-%m-%Y")}

    @classmethod
    def get_template_input_dict(
        cls,
        structure: Structure,
        namespace: Optional[StructureNamespace] = None,
        params: Dict[str, str] = {},
    ) -> Dict[str, Any]:
        """
        Get the input dictionary for template rendering based on all input parameters

        The created dictionary contains :
            - structure : A dictionary of the structure attributes, created using the get_structure_jinja_dict method
            - gen_params : A dictionary of the general parameters, including the class generic parameters
                and the parameters provided as input

        Parameters
        ----------
        structure : Structure
            The structure
        namespace : StructureNamespace
            The namespace for this structure
        params : Dict[str, str]
            The specific parameters for the generation

        Returns
        -------
            The Dictionary for template rendering
        """
        gen_param_dict = cls.get_generic_param_dict()
        gen_param_dict.update(params)
        return {
            "namespace": (namespace.as_dict() if namespace is not None else {}),
            "structure": cls.get_structure_dict_for_jinja_rendering(structure),
            "gen_params": gen_param_dict,
        }

    @classmethod
    def create_statement(
        cls,
        template: Template,
        structure: Structure,
        namespace: Optional[StructureNamespace] = None,
        params: Dict[str, str] = {},
    ) -> str:
        """
        Create a statement (stored in a string) using the provided template for the input namespace
        , structure and parameters

        Parameters
        ----------
        template : Template
            The template used for statement rendering
        structure : Structure
            The structure
        namespace : StructureNamespace
            The namespace for this structure
        params : Dict, optional
            A dictionary of parameters, which can be used by the template

        Returns
        -------
            The rendered statement
        """
        return template.render(
            cls.get_template_input_dict(
                structure=structure, namespace=namespace, params=params
            )
        )
