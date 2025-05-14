import pydantic
import typing
import typing_extensions

from .update_api_link_api_version import (
    UpdateApiLinkApiVersion,
    _SerializerUpdateApiLinkApiVersion,
)


class UpdateApiLink(typing_extensions.TypedDict):
    """
    UpdateApiLink
    """

    api_version: typing_extensions.NotRequired[UpdateApiLinkApiVersion]
    """
    the api version can only be patched on api links with a `pinned` policy
    """

    build_request_enabled: typing_extensions.NotRequired[bool]

    include_mock_server: typing_extensions.NotRequired[bool]
    """
    automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
    """

    nav_label: typing_extensions.NotRequired[str]

    policy: typing_extensions.NotRequired[typing_extensions.Literal["latest", "pinned"]]
    """
    defines how the link should be automatically updated as new API version are added
    """

    slug: typing_extensions.NotRequired[str]


class _SerializerUpdateApiLink(pydantic.BaseModel):
    """
    Serializer for UpdateApiLink handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_version: typing.Optional[_SerializerUpdateApiLinkApiVersion] = pydantic.Field(
        alias="api_version", default=None
    )
    build_request_enabled: typing.Optional[bool] = pydantic.Field(
        alias="build_request_enabled", default=None
    )
    include_mock_server: typing.Optional[bool] = pydantic.Field(
        alias="include_mock_server", default=None
    )
    nav_label: typing.Optional[str] = pydantic.Field(alias="nav_label", default=None)
    policy: typing.Optional[typing_extensions.Literal["latest", "pinned"]] = (
        pydantic.Field(alias="policy", default=None)
    )
    slug: typing.Optional[str] = pydantic.Field(alias="slug", default=None)
