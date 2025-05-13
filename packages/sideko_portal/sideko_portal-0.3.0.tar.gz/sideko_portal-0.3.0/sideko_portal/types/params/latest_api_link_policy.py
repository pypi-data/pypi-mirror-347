import pydantic
import typing_extensions


class LatestApiLinkPolicy(typing_extensions.TypedDict):
    """
    LatestApiLinkPolicy
    """

    api_id: typing_extensions.Required[str]

    type_: typing_extensions.Required[typing_extensions.Literal["latest"]]


class _SerializerLatestApiLinkPolicy(pydantic.BaseModel):
    """
    Serializer for LatestApiLinkPolicy handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_id: str = pydantic.Field(
        alias="api_id",
    )
    type_: typing_extensions.Literal["latest"] = pydantic.Field(
        alias="type",
    )
