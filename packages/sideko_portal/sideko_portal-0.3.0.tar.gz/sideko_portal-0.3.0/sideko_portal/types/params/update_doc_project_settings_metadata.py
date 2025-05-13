import pydantic
import typing
import typing_extensions


class UpdateDocProjectSettingsMetadata(typing_extensions.TypedDict):
    """
    UpdateDocProjectSettingsMetadata
    """

    description: typing_extensions.NotRequired[str]

    title: typing_extensions.NotRequired[str]


class _SerializerUpdateDocProjectSettingsMetadata(pydantic.BaseModel):
    """
    Serializer for UpdateDocProjectSettingsMetadata handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    description: typing.Optional[str] = pydantic.Field(
        alias="description", default=None
    )
    title: typing.Optional[str] = pydantic.Field(alias="title", default=None)
