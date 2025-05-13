import pydantic


class Asset(pydantic.BaseModel):
    """
    Asset
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    extension: str = pydantic.Field(
        alias="extension",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    name: str = pydantic.Field(
        alias="name",
    )
    url: str = pydantic.Field(
        alias="url",
    )
