import pydantic
import typing_extensions


class NewOrganization(typing_extensions.TypedDict):
    """
    NewOrganization
    """

    name: typing_extensions.Required[str]

    subdomain: typing_extensions.Required[str]


class _SerializerNewOrganization(pydantic.BaseModel):
    """
    Serializer for NewOrganization handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: str = pydantic.Field(
        alias="name",
    )
    subdomain: str = pydantic.Field(
        alias="subdomain",
    )
