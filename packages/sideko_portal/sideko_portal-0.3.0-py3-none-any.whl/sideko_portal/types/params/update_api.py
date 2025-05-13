import pydantic
import typing
import typing_extensions


class UpdateApi(typing_extensions.TypedDict):
    """
    Used to patch an API Specification
    """

    name: typing_extensions.NotRequired[str]


class _SerializerUpdateApi(pydantic.BaseModel):
    """
    Serializer for UpdateApi handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
