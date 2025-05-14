import pydantic
import typing

from .lint_error_details import LintErrorDetails


class ApiSpecStatsLintErrors(pydantic.BaseModel):
    """
    ApiSpecStatsLintErrors
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    incorrect_examples: typing.List[LintErrorDetails] = pydantic.Field(
        alias="incorrect_examples",
    )
    incorrect_paths: typing.List[str] = pydantic.Field(
        alias="incorrect_paths",
    )
    missing_operation_ids: typing.List[LintErrorDetails] = pydantic.Field(
        alias="missing_operation_ids",
    )
