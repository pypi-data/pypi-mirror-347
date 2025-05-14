import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from jinja2 import Template

from nexuslabdata.core.structure.sql_template_wrapper import SQLTemplateWrapper
from nexuslabdata.core.structure.structure import Structure
from nexuslabdata.core.structure.structure_adapter import StructureAdapter
from nexuslabdata.exceptions import MissingObjectException
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn
from nexuslabdata.utils.jinja_utils import get_template_variables


@dataclass
class SQLRenderEntry(NldNamedDataClassMixIn):
    name: str = ""
    file_name_pattern: str = ""
    adapter: Optional[StructureAdapter] = None

    DEFAULT_PATTERN = "{{ structure_name }}.sql"

    def _suffix_from_name(self) -> str:
        """Extracts the suffix from a template filename."""
        base = os.path.basename(self.name)
        match = re.match(r".*\.([^.]+)\.sql$", base, flags=re.IGNORECASE)
        return (
            match.group(1).lower()
            if match
            else os.path.splitext(base)[0].lower()
        )

    def build_filename(
        self, structure_name: str, params: Dict[str, str]
    ) -> str:
        """Constructs the final filename according to the version pattern."""
        pattern = self.file_name_pattern or self.DEFAULT_PATTERN
        context = {
            **params,
            "structure_name": structure_name,
            "suffix": self._suffix_from_name(),
        }
        expected_params = get_template_variables(pattern)
        missing_params = expected_params - context.keys()
        if missing_params:
            raise ValueError(
                f"Missing parameters for file name pattern: {missing_params}."
            )

        try:
            return Template(pattern).render(**context).strip()
        except Exception as e:
            raise ValueError(
                f"Failed to render file name with pattern '{self.file_name_pattern}': {e}"
            ) from e


@dataclass
class SQLRendererWrapper(NldNamedDataClassMixIn):
    name: str = ""
    renderer: List[SQLRenderEntry] = field(default_factory=list)

    def render_all(
        self,
        structure: Structure,
        params: Dict[str, str],
        output_folder: str,
        templates_dict: Dict[str, SQLTemplateWrapper],
        adapters_dict: Dict[str, StructureAdapter],
    ) -> None:
        """Renders all SQL templates for the given structure."""
        for entry in self.renderer:
            template_wrapper = templates_dict.get(entry.name)
            if template_wrapper is None:
                raise MissingObjectException(SQLTemplateWrapper, entry.name)

            adapter_obj: Optional[StructureAdapter] = None
            if entry.adapter:
                key = entry.adapter.name
                adapter_obj = adapters_dict.get(key)
                if adapter_obj is None:
                    raise MissingObjectException(StructureAdapter, key)

            wrapper = SQLTemplateWrapper(
                name=entry.name,
                template=template_wrapper.template,
                structure_adapter=adapter_obj,
            )

            file_name = entry.build_filename(structure.name, params)

            try:
                wrapper.generate_sql(structure, output_folder, file_name)
            except Exception as e:
                raise ValueError(
                    f"Failed to render SQL statement for {entry.name}: {e}"
                ) from e
