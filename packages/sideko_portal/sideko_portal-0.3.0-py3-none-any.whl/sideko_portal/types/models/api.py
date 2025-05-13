import pydantic


class Api(pydantic.BaseModel):
    """
    Api
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    created_at: str = pydantic.Field(
        alias="created_at",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    name: str = pydantic.Field(
        alias="name",
    )
    version_count: int = pydantic.Field(
        alias="version_count",
    )
    """
    number of versions in the API, including all pre-release versions
    """
