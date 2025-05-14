import pydantic
import typing_extensions


class CliUpdate(pydantic.BaseModel):
    """
    CliUpdate
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    message: str = pydantic.Field(
        alias="message",
    )
    severity: typing_extensions.Literal["info", "required", "suggested"] = (
        pydantic.Field(
            alias="severity",
        )
    )
