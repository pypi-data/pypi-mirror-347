import pydantic


class ApiLinkReorder(pydantic.BaseModel):
    """
    ApiLinkReorder
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    group_id: str = pydantic.Field(
        alias="group_id",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    order: int = pydantic.Field(
        alias="order",
    )
