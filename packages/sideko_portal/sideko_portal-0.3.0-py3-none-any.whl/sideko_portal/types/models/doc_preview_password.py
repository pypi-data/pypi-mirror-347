import pydantic


class DocPreviewPassword(pydantic.BaseModel):
    """
    DocPreviewPassword
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    name: str = pydantic.Field(
        alias="name",
    )
    password: str = pydantic.Field(
        alias="password",
    )
