import pydantic
import typing_extensions


class UpdateApiLinkApiVersion(typing_extensions.TypedDict):
    """
    the api version can only be patched on api links with a `pinned` policy
    """

    api_id: typing_extensions.Required[str]

    version: typing_extensions.Required[str]


class _SerializerUpdateApiLinkApiVersion(pydantic.BaseModel):
    """
    Serializer for UpdateApiLinkApiVersion handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_id: str = pydantic.Field(
        alias="api_id",
    )
    version: str = pydantic.Field(
        alias="version",
    )
