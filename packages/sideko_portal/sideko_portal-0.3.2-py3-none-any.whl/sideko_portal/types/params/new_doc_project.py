import pydantic
import typing_extensions


class NewDocProject(typing_extensions.TypedDict):
    """
    NewDocProject
    """

    name: typing_extensions.Required[str]


class _SerializerNewDocProject(pydantic.BaseModel):
    """
    Serializer for NewDocProject handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: str = pydantic.Field(
        alias="name",
    )
