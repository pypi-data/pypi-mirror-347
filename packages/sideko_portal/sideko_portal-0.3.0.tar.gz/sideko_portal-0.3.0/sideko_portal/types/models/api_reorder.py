import pydantic
import typing

from .api_link_group_reorder import ApiLinkGroupReorder
from .api_link_reorder import ApiLinkReorder


class ApiReorder(pydantic.BaseModel):
    """
    ApiReorder
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    doc_version_id: str = pydantic.Field(
        alias="doc_version_id",
    )
    groups: typing.List[ApiLinkGroupReorder] = pydantic.Field(
        alias="groups",
    )
    links: typing.List[ApiLinkReorder] = pydantic.Field(
        alias="links",
    )
