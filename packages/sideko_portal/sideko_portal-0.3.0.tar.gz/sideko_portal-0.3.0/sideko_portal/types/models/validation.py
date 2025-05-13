import pydantic
import typing_extensions


class Validation(pydantic.BaseModel):
    """
    Validation
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    message: str = pydantic.Field(
        alias="message",
    )
    """
    description of the validation issue
    """
    severity: typing_extensions.Literal["error", "info", "warning"] = pydantic.Field(
        alias="severity",
    )
