import pydantic
import typing_extensions

from .lint_location import LintLocation


class LintResult(pydantic.BaseModel):
    """
    LintResult
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    category: str = pydantic.Field(
        alias="category",
    )
    how_to_fix: str = pydantic.Field(
        alias="how_to_fix",
    )
    location: LintLocation = pydantic.Field(
        alias="location",
    )
    message: str = pydantic.Field(
        alias="message",
    )
    rule: str = pydantic.Field(
        alias="rule",
    )
    severity: typing_extensions.Literal["error", "info", "unknown", "warn"] = (
        pydantic.Field(
            alias="severity",
        )
    )
