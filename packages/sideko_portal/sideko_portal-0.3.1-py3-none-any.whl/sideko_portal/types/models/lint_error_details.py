import pydantic
import typing


class LintErrorDetails(pydantic.BaseModel):
    """
    Describes the problems found by the Sideko OpenAPI linter
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    location: typing.Optional[str] = pydantic.Field(
        alias="location",
    )
    message: typing.Optional[str] = pydantic.Field(
        alias="message",
    )
    method: str = pydantic.Field(
        alias="method",
    )
    path: str = pydantic.Field(
        alias="path",
    )
