from nexuslabdata.connection.base.connection_info import (
    ConnectionInfo,
    ConnectionInfos,
)

DEFAULT_YAML_FILE_CONTENT = """# Connections configurations

#connections:
#    snow_dummy:
#        name: snow_dummy
#        type: snowflake
#        default_profile: local
#        profiles:
#            local:
#                account: "dummy.eu-west-3.aws"
#                user: "OPENDATA_USER"
#                password: "OPENDATA_PASSWORD"
"""


def get_default() -> ConnectionInfos:
    return ConnectionInfos(
        connections={
            "snow_dummy": ConnectionInfo(
                "snow_dummy",
                "snowflake",
                "local",
                {
                    "local": {
                        "account": "dummy.eu-west-3.aws",
                        "user": "OPENDATA_USER",
                        "password": "OPENDATA_PASSWORD",
                    }
                },
            )
        }
    )
