import pydantic


class ApiLinkGroupReorder(pydantic.BaseModel):
    """
    ApiLinkGroupReorder
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    id: str = pydantic.Field(
        alias="id",
    )
    order: int = pydantic.Field(
        alias="order",
    )
