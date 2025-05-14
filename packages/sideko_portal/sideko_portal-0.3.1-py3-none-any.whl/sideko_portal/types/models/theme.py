import pydantic
import typing_extensions

from .theme_values import ThemeValues


class Theme(pydantic.BaseModel):
    """
    Theme
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    owner: typing_extensions.Literal["default", "organization", "self"] = (
        pydantic.Field(
            alias="owner",
        )
    )
    values: ThemeValues = pydantic.Field(
        alias="values",
    )
