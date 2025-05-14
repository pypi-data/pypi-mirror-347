import pydantic
import typing
import typing_extensions


class UpdateDocProjectLogos(typing_extensions.TypedDict):
    """
    UpdateDocProjectLogos
    """

    dark: typing_extensions.NotRequired[str]
    """
    asset id of dark logo
    """

    favicon: typing_extensions.NotRequired[str]
    """
    asset id of favicon
    """

    light: typing_extensions.NotRequired[str]
    """
    asset id of light logo
    """


class _SerializerUpdateDocProjectLogos(pydantic.BaseModel):
    """
    Serializer for UpdateDocProjectLogos handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    dark: typing.Optional[str] = pydantic.Field(alias="dark", default=None)
    favicon: typing.Optional[str] = pydantic.Field(alias="favicon", default=None)
    light: typing.Optional[str] = pydantic.Field(alias="light", default=None)
