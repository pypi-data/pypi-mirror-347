import pydantic
import typing
import typing_extensions

from .validation import Validation


class OpenApi(pydantic.BaseModel):
    """
    OpenApi
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    extension: typing_extensions.Literal["json", "yaml"] = pydantic.Field(
        alias="extension",
    )
    is_config_valid: bool = pydantic.Field(
        alias="is_config_valid",
    )
    """
    Are the various the Sideko configuration (x-fields) valid
    """
    is_valid: bool = pydantic.Field(
        alias="is_valid",
    )
    """
    Is the OpenAPI spec a valid 3.x spec
    """
    openapi: str = pydantic.Field(
        alias="openapi",
    )
    """
    OpenAPI content as a string in JSON format
    """
    validations: typing.List[Validation] = pydantic.Field(
        alias="validations",
    )
