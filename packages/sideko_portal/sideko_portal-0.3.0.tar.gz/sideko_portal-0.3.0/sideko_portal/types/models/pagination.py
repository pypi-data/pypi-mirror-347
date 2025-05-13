import pydantic


class Pagination(pydantic.BaseModel):
    """
    Pagination
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    page: int = pydantic.Field(
        alias="page",
    )
    """
    current page
    """
    page_count: int = pydantic.Field(
        alias="page_count",
    )
    """
    total number of pages
    """
    page_limit: int = pydantic.Field(
        alias="page_limit",
    )
    """
    maximum number of results per page
    """
    total_count: int = pydantic.Field(
        alias="total_count",
    )
    """
    total number of results across all pages
    """
