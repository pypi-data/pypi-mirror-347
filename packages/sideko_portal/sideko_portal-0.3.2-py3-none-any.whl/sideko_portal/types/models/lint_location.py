import pydantic


class LintLocation(pydantic.BaseModel):
    """
    LintLocation
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    end_column: int = pydantic.Field(
        alias="end_column",
    )
    end_line: int = pydantic.Field(
        alias="end_line",
    )
    path: str = pydantic.Field(
        alias="path",
    )
    start_column: int = pydantic.Field(
        alias="start_column",
    )
    start_line: int = pydantic.Field(
        alias="start_line",
    )
