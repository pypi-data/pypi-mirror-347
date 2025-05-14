import pydantic
import typing_extensions


class NewApi(typing_extensions.TypedDict):
    """
    NewApi
    """

    name: typing_extensions.Required[str]


class _SerializerNewApi(pydantic.BaseModel):
    """
    Serializer for NewApi handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: str = pydantic.Field(
        alias="name",
    )
