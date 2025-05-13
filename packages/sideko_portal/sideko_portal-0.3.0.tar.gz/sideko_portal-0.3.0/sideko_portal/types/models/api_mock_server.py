import pydantic


class ApiMockServer(pydantic.BaseModel):
    """
    ApiMockServer
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    enabled: bool = pydantic.Field(
        alias="enabled",
    )
    url: str = pydantic.Field(
        alias="url",
    )
