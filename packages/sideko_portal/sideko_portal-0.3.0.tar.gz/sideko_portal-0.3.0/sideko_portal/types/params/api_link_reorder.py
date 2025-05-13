import pydantic
import typing_extensions


class ApiLinkReorder(typing_extensions.TypedDict):
    """
    ApiLinkReorder
    """

    group_id: typing_extensions.Required[str]

    id: typing_extensions.Required[str]

    order: typing_extensions.Required[int]


class _SerializerApiLinkReorder(pydantic.BaseModel):
    """
    Serializer for ApiLinkReorder handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    group_id: str = pydantic.Field(
        alias="group_id",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    order: int = pydantic.Field(
        alias="order",
    )
