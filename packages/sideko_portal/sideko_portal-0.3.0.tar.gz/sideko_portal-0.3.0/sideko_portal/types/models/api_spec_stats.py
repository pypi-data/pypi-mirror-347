import pydantic
import typing

from .api_spec_stats_lint_errors import ApiSpecStatsLintErrors


class ApiSpecStats(pydantic.BaseModel):
    """
    ApiSpecStats
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    authenticated_methods: int = pydantic.Field(
        alias="authenticated_methods",
    )
    """
    Total Authenticated Methods (operations)
    """
    authentication_schemes: typing.List[str] = pydantic.Field(
        alias="authentication_schemes",
    )
    """
    A description of all defined auth schemes
    """
    endpoints: int = pydantic.Field(
        alias="endpoints",
    )
    """
    Total Endpoints (paths)
    """
    lint_errors: ApiSpecStatsLintErrors = pydantic.Field(
        alias="lint_errors",
    )
    methods: int = pydantic.Field(
        alias="methods",
    )
    """
    Total Methods (operations)
    """
    public_methods: int = pydantic.Field(
        alias="public_methods",
    )
    """
    Total Unauthenticated Methods (operations)
    """
    response_codes: typing.List[int] = pydantic.Field(
        alias="response_codes",
    )
    """
    All Response Codes (not deduplicated)
    """
