import pydantic
import typing_extensions

from .api_link_api_version import ApiLinkApiVersion
from .api_link_doc_version import ApiLinkDocVersion


class ApiLink(pydantic.BaseModel):
    """
    ApiLink
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    api_version: ApiLinkApiVersion = pydantic.Field(
        alias="api_version",
    )
    """
    Summary object of the api version included in the api link
    """
    build_request_enabled: bool = pydantic.Field(
        alias="build_request_enabled",
    )
    created_at: str = pydantic.Field(
        alias="created_at",
    )
    doc_version: ApiLinkDocVersion = pydantic.Field(
        alias="doc_version",
    )
    """
    Summary object of the doc version included in the api link
    """
    group_id: str = pydantic.Field(
        alias="group_id",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    include_mock_server: bool = pydantic.Field(
        alias="include_mock_server",
    )
    """
    automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
    """
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
    order: int = pydantic.Field(
        alias="order",
    )
    policy: typing_extensions.Literal["latest", "pinned"] = pydantic.Field(
        alias="policy",
    )
    """
    defines how the link should be automatically updated as new API version are added
    """
    slug: str = pydantic.Field(
        alias="slug",
    )
