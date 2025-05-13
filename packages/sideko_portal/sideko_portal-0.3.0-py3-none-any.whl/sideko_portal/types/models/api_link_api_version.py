import pydantic


class ApiLinkApiVersion(pydantic.BaseModel):
    """
    Summary object of the api version included in the api link
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    api_id: str = pydantic.Field(
        alias="api_id",
    )
    api_name: str = pydantic.Field(
        alias="api_name",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    version: str = pydantic.Field(
        alias="version",
    )
