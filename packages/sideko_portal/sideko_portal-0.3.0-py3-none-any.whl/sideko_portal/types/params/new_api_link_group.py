import pydantic
import typing_extensions


class NewApiLinkGroup(typing_extensions.TypedDict):
    """
    NewApiLinkGroup
    """

    doc_version_id: typing_extensions.Required[str]

    nav_label: typing_extensions.Required[str]

    slug: typing_extensions.Required[str]


class _SerializerNewApiLinkGroup(pydantic.BaseModel):
    """
    Serializer for NewApiLinkGroup handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    doc_version_id: str = pydantic.Field(
        alias="doc_version_id",
    )
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
    slug: str = pydantic.Field(
        alias="slug",
    )
