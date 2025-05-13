import pydantic


class LintSummary(pydantic.BaseModel):
    """
    LintSummary
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    errors: int = pydantic.Field(
        alias="errors",
    )
    infos: int = pydantic.Field(
        alias="infos",
    )
    warns: int = pydantic.Field(
        alias="warns",
    )
