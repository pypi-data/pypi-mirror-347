import pydantic
import typing_extensions


class PinnedApiLinkPolicy(typing_extensions.TypedDict):
    """
    PinnedApiLinkPolicy
    """

    api_id: typing_extensions.Required[str]

    api_version: typing_extensions.Required[str]

    type_: typing_extensions.Required[typing_extensions.Literal["pinned"]]


class _SerializerPinnedApiLinkPolicy(pydantic.BaseModel):
    """
    Serializer for PinnedApiLinkPolicy handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_id: str = pydantic.Field(
        alias="api_id",
    )
    api_version: str = pydantic.Field(
        alias="api_version",
    )
    type_: typing_extensions.Literal["pinned"] = pydantic.Field(
        alias="type",
    )
