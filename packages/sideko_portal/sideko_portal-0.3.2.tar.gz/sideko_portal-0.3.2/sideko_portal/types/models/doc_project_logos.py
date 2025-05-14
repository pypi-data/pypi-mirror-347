import pydantic
import typing

from .asset import Asset


class DocProjectLogos(pydantic.BaseModel):
    """
    DocProjectLogos
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    dark: typing.Optional[Asset] = pydantic.Field(
        alias="dark",
    )
    favicon: typing.Optional[Asset] = pydantic.Field(
        alias="favicon",
    )
    light: typing.Optional[Asset] = pydantic.Field(
        alias="light",
    )
