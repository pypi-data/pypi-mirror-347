import pydantic
import typing
import typing_extensions

from .latest_api_link_policy import LatestApiLinkPolicy, _SerializerLatestApiLinkPolicy
from .pinned_api_link_policy import PinnedApiLinkPolicy, _SerializerPinnedApiLinkPolicy


class NewApiLink(typing_extensions.TypedDict):
    """
    NewApiLink
    """

    build_request_enabled: typing_extensions.NotRequired[bool]

    doc_version_id: typing_extensions.Required[str]

    group_id: typing_extensions.Required[str]

    include_mock_server: typing_extensions.NotRequired[bool]
    """
    automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
    """

    nav_label: typing_extensions.Required[str]

    policy: typing_extensions.Required[
        typing.Union[LatestApiLinkPolicy, PinnedApiLinkPolicy]
    ]

    slug: typing_extensions.Required[str]


class _SerializerNewApiLink(pydantic.BaseModel):
    """
    Serializer for NewApiLink handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    build_request_enabled: typing.Optional[bool] = pydantic.Field(
        alias="build_request_enabled", default=None
    )
    doc_version_id: str = pydantic.Field(
        alias="doc_version_id",
    )
    group_id: str = pydantic.Field(
        alias="group_id",
    )
    include_mock_server: typing.Optional[bool] = pydantic.Field(
        alias="include_mock_server", default=None
    )
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
    policy: typing.Union[
        _SerializerLatestApiLinkPolicy, _SerializerPinnedApiLinkPolicy
    ] = pydantic.Field(
        alias="policy",
    )
    slug: str = pydantic.Field(
        alias="slug",
    )
