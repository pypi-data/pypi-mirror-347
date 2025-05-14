import pydantic
import typing
import typing_extensions


class UpdateApiLinkGroup(typing_extensions.TypedDict):
    """
    UpdateApiLinkGroup
    """

    nav_label: typing_extensions.NotRequired[str]

    slug: typing_extensions.NotRequired[str]


class _SerializerUpdateApiLinkGroup(pydantic.BaseModel):
    """
    Serializer for UpdateApiLinkGroup handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    nav_label: typing.Optional[str] = pydantic.Field(alias="nav_label", default=None)
    slug: typing.Optional[str] = pydantic.Field(alias="slug", default=None)
