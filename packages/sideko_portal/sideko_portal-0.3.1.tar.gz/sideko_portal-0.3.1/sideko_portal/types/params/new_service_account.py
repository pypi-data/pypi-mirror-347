import pydantic
import typing
import typing_extensions

from .object_role import ObjectRole, _SerializerObjectRole


class NewServiceAccount(typing_extensions.TypedDict):
    """
    NewServiceAccount
    """

    expiration: typing_extensions.NotRequired[str]
    """
    UTC datetime when the service account key should expire (ISO 8601 format without timezone), key never expires expiration is not specified
    """

    name: typing_extensions.Required[str]

    object_roles: typing_extensions.Required[typing.List[ObjectRole]]


class _SerializerNewServiceAccount(pydantic.BaseModel):
    """
    Serializer for NewServiceAccount handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    expiration: typing.Optional[str] = pydantic.Field(alias="expiration", default=None)
    name: str = pydantic.Field(
        alias="name",
    )
    object_roles: typing.List[_SerializerObjectRole] = pydantic.Field(
        alias="object_roles",
    )
