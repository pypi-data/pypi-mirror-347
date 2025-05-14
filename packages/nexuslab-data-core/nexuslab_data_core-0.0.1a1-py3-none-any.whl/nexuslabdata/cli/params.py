import click

from nexuslabdata.utils import decorator_utils

connection_name = click.option(
    "--connection-name",
    type=str,
    envvar=None,
    help="Connection name to use",
    default=None,
    required=True,
)
profile_name = click.option(
    "--profile-name",
    type=str,
    envvar=None,
    help="Profile name to use",
    default=None,
    required=False,
)

specific_connection_params = decorator_utils.composed(
    connection_name, profile_name
)

# Option pour --params-file
data_flow_name = click.option(
    "--data-flow-name",
    required=True,
    help="Name of the data flow",
)

# Option pour --env
profile_name = click.option(
    "--profile-name",
    required=True,
    help="Profile to use",
)

structure = click.option(
    "--structure",
    required=True,
    help="Structure name inside the structure folder",
)

renderer = click.option(
    "--renderer",
    required=True,
    help="Renderer folder name inside sql_templates",
)


output_folder_name_not_required = click.option(
    "--output-folder-name",
    required=False,
    default=None,
    help="Optional output folder name",
)

params = click.option(
    "--params",
    required=False,
    default="",
    help="Optional key-value parameters for file naming, e.g.: 'MAJOR=1,MINOR=2'",
)

specific_sql_renderer_params = decorator_utils.composed(
    structure, renderer, output_folder_name_not_required, params
)

adapter = click.option(
    "--adapter",
    required=True,
    help="Adapter name inside the adapter folder",
)

specific_structure_build_params = decorator_utils.composed(
    adapter, structure, output_folder_name_not_required
)


specific_structure_convert_to_yaml_params = decorator_utils.composed(
    structure, output_folder_name_not_required
)
