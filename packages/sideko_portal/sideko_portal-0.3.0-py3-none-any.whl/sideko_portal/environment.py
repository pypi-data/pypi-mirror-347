import enum
import typing


class Environment(enum.Enum):
    """Pre-defined base URLs for the API"""

    PRODUCTION = "https://api.sideko.dev/v1"
    MOCK_SERVER = (
        "https://api.sideko-staging.dev/v1/mock/sideko-octa/sideko-portal/2.4.0"
    )


def _get_base_url(
    *, base_url: typing.Optional[str] = None, environment: Environment
) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Must include a base_url or environment arguments")
