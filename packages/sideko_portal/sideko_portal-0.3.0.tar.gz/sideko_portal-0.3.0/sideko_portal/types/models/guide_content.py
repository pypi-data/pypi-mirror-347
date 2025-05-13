import pydantic


class GuideContent(pydantic.BaseModel):
    """
    GuideContent
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    content: str = pydantic.Field(
        alias="content",
    )
