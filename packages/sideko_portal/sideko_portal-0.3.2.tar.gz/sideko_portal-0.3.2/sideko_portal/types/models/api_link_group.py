import pydantic


class ApiLinkGroup(pydantic.BaseModel):
    """
    ApiLinkGroup
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    doc_version_id: str = pydantic.Field(
        alias="doc_version_id",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
    order: int = pydantic.Field(
        alias="order",
    )
    slug: str = pydantic.Field(
        alias="slug",
    )
