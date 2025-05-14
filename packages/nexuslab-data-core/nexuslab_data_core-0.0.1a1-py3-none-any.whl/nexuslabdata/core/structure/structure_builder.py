import os
from dataclasses import dataclass
from typing import Optional

from nexuslabdata.core import Structure, StructureAdapter, StructureCsvAdapter
from nexuslabdata.utils.data_class_mixin import NldNamedDataClassMixIn
from nexuslabdata.utils.datetime_util import (
    get_current_datetime_as_filesystem_friendly_str,
)
from nexuslabdata.utils.yaml_util import dump_dict_to_yaml


@dataclass
class StructureBuilder(NldNamedDataClassMixIn):
    structure: Structure
    structure_adapter: StructureAdapter
    output_folder_name: Optional[str] = None

    def structure_builder(self) -> None:
        """
        Builds and writes a new data structure into YAML and CSV formats.
        """
        folder_name = (
            self.output_folder_name
            or get_current_datetime_as_filesystem_friendly_str()
        )

        new_structure = self.structure_adapter.adapt_structure(
            original_structure=self.structure
        )
        data_dict = new_structure.to_dict()

        # Create output directory
        output_dir = os.path.join("output", folder_name)
        os.makedirs(output_dir, exist_ok=True)

        # Dump yaml
        yaml_path = os.path.join(output_dir, f"{new_structure.name}.yml")
        dump_dict_to_yaml(data_dict, yaml_path)

        # Dump csv
        csv_path = os.path.join(output_dir, f"{new_structure.name}.csv")
        StructureCsvAdapter().to_csv(
            file_path=csv_path,
            obj=[new_structure],
        )

        self.log_debug(f"New Structure generated in {yaml_path}")
        return
