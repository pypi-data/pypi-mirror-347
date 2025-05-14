import os
from dataclasses import dataclass
from typing import Optional

from jinja2 import Template

from nexuslabdata.core.structure.structure import Structure
from nexuslabdata.core.structure.structure_adapter import StructureAdapter
from nexuslabdata.core.structure.structure_sql_renderer import (
    StructureSqlRenderer,
)
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn
from nexuslabdata.utils.datetime_util import (
    get_current_datetime_as_filesystem_friendly_str,
)


@dataclass
class SQLTemplateWrapper(NldNamedDataClassMixIn):
    name: str = ""
    template: str = ""
    structure_adapter: Optional[StructureAdapter] = None

    def generate_sql(
        self,
        structure: Structure,
        output_folder: str,
        file_name: str,
    ) -> None:
        """
        Generates an SQL file by rendering the template with the given structure.
        """
        folder_name = (
            output_folder or get_current_datetime_as_filesystem_friendly_str()
        )

        structure_to_render = (
            self.structure_adapter.adapt_structure(original_structure=structure)
            if self.structure_adapter
            else structure
        )

        try:
            sql_statement = StructureSqlRenderer.create_statement(
                template=Template(self.template),
                structure=structure_to_render,
            )
        except Exception as e:
            raise ValueError(f"Failed to render SQL statement: {e}") from e

        output_dir = os.path.join("output", folder_name)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(sql_statement)

        self.log_info(f"SQL generated in {output_path}")
