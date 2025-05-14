import pydantic

from .api import Api
from .api_mock_server import ApiMockServer


class ApiSpec(pydantic.BaseModel):
    """
    ApiSpec
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    api: Api = pydantic.Field(
        alias="api",
    )
    created_at: str = pydantic.Field(
        alias="created_at",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    mock_server: ApiMockServer = pydantic.Field(
        alias="mock_server",
    )
    notes: str = pydantic.Field(
        alias="notes",
    )
    """
    Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
    """
    version: str = pydantic.Field(
        alias="version",
    )
