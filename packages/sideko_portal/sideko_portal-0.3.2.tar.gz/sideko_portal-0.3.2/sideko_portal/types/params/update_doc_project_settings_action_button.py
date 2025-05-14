import pydantic
import typing
import typing_extensions


class UpdateDocProjectSettingsActionButton(typing_extensions.TypedDict):
    """
    UpdateDocProjectSettingsActionButton
    """

    enabled: typing_extensions.NotRequired[bool]

    label: typing_extensions.NotRequired[str]

    url: typing_extensions.NotRequired[str]


class _SerializerUpdateDocProjectSettingsActionButton(pydantic.BaseModel):
    """
    Serializer for UpdateDocProjectSettingsActionButton handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    enabled: typing.Optional[bool] = pydantic.Field(alias="enabled", default=None)
    label: typing.Optional[str] = pydantic.Field(alias="label", default=None)
    url: typing.Optional[str] = pydantic.Field(alias="url", default=None)
