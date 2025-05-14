import pydantic
import typing
import typing_extensions


class ReorderGuide(typing_extensions.TypedDict):
    """
    ReorderGuide
    """

    id: typing_extensions.Required[str]

    order: typing_extensions.Required[int]

    parent_id: typing_extensions.Required[typing.Optional[str]]


class _SerializerReorderGuide(pydantic.BaseModel):
    """
    Serializer for ReorderGuide handling case conversions
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
    parent_id: typing.Optional[str] = pydantic.Field(
        alias="parent_id",
    )
