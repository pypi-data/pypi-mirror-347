import pydantic
import typing
import typing_extensions


class ThemeValues(typing_extensions.TypedDict):
    """
    ThemeValues
    """

    api_reference_group_variant: typing_extensions.NotRequired[typing.Optional[str]]
    """
    set a group variant to collapse all of references under one dropdown in the sidebar
    """

    dark_active_button_bg_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    dark_active_button_text_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    dark_bg_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    dark_navbar_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    dark_navbar_text_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    light_active_button_bg_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    light_active_button_text_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    light_bg_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    light_navbar_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """

    light_navbar_text_color: typing_extensions.NotRequired[typing.Optional[str]]
    """
    in HEX format
    """


class _SerializerThemeValues(pydantic.BaseModel):
    """
    Serializer for ThemeValues handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_reference_group_variant: typing.Optional[str] = pydantic.Field(
        alias="api_reference_group_variant", default=None
    )
    dark_active_button_bg_color: typing.Optional[str] = pydantic.Field(
        alias="dark_active_button_bg_color", default=None
    )
    dark_active_button_text_color: typing.Optional[str] = pydantic.Field(
        alias="dark_active_button_text_color", default=None
    )
    dark_bg_color: typing.Optional[str] = pydantic.Field(
        alias="dark_bg_color", default=None
    )
    dark_navbar_color: typing.Optional[str] = pydantic.Field(
        alias="dark_navbar_color", default=None
    )
    dark_navbar_text_color: typing.Optional[str] = pydantic.Field(
        alias="dark_navbar_text_color", default=None
    )
    light_active_button_bg_color: typing.Optional[str] = pydantic.Field(
        alias="light_active_button_bg_color", default=None
    )
    light_active_button_text_color: typing.Optional[str] = pydantic.Field(
        alias="light_active_button_text_color", default=None
    )
    light_bg_color: typing.Optional[str] = pydantic.Field(
        alias="light_bg_color", default=None
    )
    light_navbar_color: typing.Optional[str] = pydantic.Field(
        alias="light_navbar_color", default=None
    )
    light_navbar_text_color: typing.Optional[str] = pydantic.Field(
        alias="light_navbar_text_color", default=None
    )
