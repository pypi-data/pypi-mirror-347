import pydantic
import typing
import typing_extensions

from .api_link_group_reorder import ApiLinkGroupReorder, _SerializerApiLinkGroupReorder
from .api_link_reorder import ApiLinkReorder, _SerializerApiLinkReorder


class ApiReorder(typing_extensions.TypedDict):
    """
    ApiReorder
    """

    doc_version_id: typing_extensions.Required[str]

    groups: typing_extensions.Required[typing.List[ApiLinkGroupReorder]]

    links: typing_extensions.Required[typing.List[ApiLinkReorder]]


class _SerializerApiReorder(pydantic.BaseModel):
    """
    Serializer for ApiReorder handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    doc_version_id: str = pydantic.Field(
        alias="doc_version_id",
    )
    groups: typing.List[_SerializerApiLinkGroupReorder] = pydantic.Field(
        alias="groups",
    )
    links: typing.List[_SerializerApiLinkReorder] = pydantic.Field(
        alias="links",
    )
