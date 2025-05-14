import pydantic


class ApiLinkDocVersion(pydantic.BaseModel):
    """
    Summary object of the doc version included in the api link
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    doc_project_id: str = pydantic.Field(
        alias="doc_project_id",
    )
    doc_project_name: str = pydantic.Field(
        alias="doc_project_name",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    version: int = pydantic.Field(
        alias="version",
    )
