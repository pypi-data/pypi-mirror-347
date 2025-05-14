import pydantic


class GuideHref(pydantic.BaseModel):
    """
    GuideHref
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    id: str = pydantic.Field(
        alias="id",
    )
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
