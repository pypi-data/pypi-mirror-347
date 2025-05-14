import pydantic
import typing_extensions


class ApiLinkGroupReorder(typing_extensions.TypedDict):
    """
    ApiLinkGroupReorder
    """

    id: typing_extensions.Required[str]

    order: typing_extensions.Required[int]


class _SerializerApiLinkGroupReorder(pydantic.BaseModel):
    """
    Serializer for ApiLinkGroupReorder handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    id: str = pydantic.Field(
        alias="id",
    )
    order: int = pydantic.Field(
        alias="order",
    )
