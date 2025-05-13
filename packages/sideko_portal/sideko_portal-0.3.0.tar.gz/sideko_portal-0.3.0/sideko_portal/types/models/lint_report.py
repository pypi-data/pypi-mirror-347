import pydantic
import typing

from .lint_result import LintResult
from .lint_summary import LintSummary


class LintReport(pydantic.BaseModel):
    """
    LintReport
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    results: typing.List[LintResult] = pydantic.Field(
        alias="results",
    )
    summary: LintSummary = pydantic.Field(
        alias="summary",
    )
