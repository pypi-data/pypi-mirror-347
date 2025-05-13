import pydantic
import typing


class ThemeValues(pydantic.BaseModel):
    """
    ThemeValues
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    api_reference_group_variant: typing.Optional[str] = pydantic.Field(
        alias="api_reference_group_variant", default=None
    )
    """
    set a group variant to collapse all of references under one dropdown in the sidebar
    """
    dark_active_button_bg_color: typing.Optional[str] = pydantic.Field(
        alias="dark_active_button_bg_color", default=None
    )
    """
    in HEX format
    """
    dark_active_button_text_color: typing.Optional[str] = pydantic.Field(
        alias="dark_active_button_text_color", default=None
    )
    """
    in HEX format
    """
    dark_bg_color: typing.Optional[str] = pydantic.Field(
        alias="dark_bg_color", default=None
    )
    """
    in HEX format
    """
    dark_navbar_color: typing.Optional[str] = pydantic.Field(
        alias="dark_navbar_color", default=None
    )
    """
    in HEX format
    """
    dark_navbar_text_color: typing.Optional[str] = pydantic.Field(
        alias="dark_navbar_text_color", default=None
    )
    """
    in HEX format
    """
    light_active_button_bg_color: typing.Optional[str] = pydantic.Field(
        alias="light_active_button_bg_color", default=None
    )
    """
    in HEX format
    """
    light_active_button_text_color: typing.Optional[str] = pydantic.Field(
        alias="light_active_button_text_color", default=None
    )
    """
    in HEX format
    """
    light_bg_color: typing.Optional[str] = pydantic.Field(
        alias="light_bg_color", default=None
    )
    """
    in HEX format
    """
    light_navbar_color: typing.Optional[str] = pydantic.Field(
        alias="light_navbar_color", default=None
    )
    """
    in HEX format
    """
    light_navbar_text_color: typing.Optional[str] = pydantic.Field(
        alias="light_navbar_text_color", default=None
    )
    """
    in HEX format
    """
