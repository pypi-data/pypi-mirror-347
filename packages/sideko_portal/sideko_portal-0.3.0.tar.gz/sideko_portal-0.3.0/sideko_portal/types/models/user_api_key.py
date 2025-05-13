import pydantic
import typing


class UserApiKey(pydantic.BaseModel):
    """
    UserApiKey
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    avatar_url: str = pydantic.Field(
        alias="avatar_url",
    )
    created_at: str = pydantic.Field(
        alias="created_at",
    )
    email: str = pydantic.Field(
        alias="email",
    )
    expiration: typing.Optional[str] = pydantic.Field(
        alias="expiration",
    )
    first_name: str = pydantic.Field(
        alias="first_name",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    is_service_account: bool = pydantic.Field(
        alias="is_service_account",
    )
    last_name: str = pydantic.Field(
        alias="last_name",
    )
    api_key: str = pydantic.Field(
        alias="api_key",
    )
