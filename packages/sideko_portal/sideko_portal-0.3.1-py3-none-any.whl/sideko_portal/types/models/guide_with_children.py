import pydantic
import typing


class GuideWithChildren(pydantic.BaseModel):
    """
    GuideWithChildren
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    created_at: str = pydantic.Field(
        alias="created_at",
    )
    icon: typing.Optional[str] = pydantic.Field(
        alias="icon",
    )
    """
    lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
    """
    id: str = pydantic.Field(
        alias="id",
    )
    is_parent: bool = pydantic.Field(
        alias="is_parent",
    )
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
    """
    the label that shows on the navbar for this guide
    """
    order: int = pydantic.Field(
        alias="order",
    )
    parent_id: typing.Optional[str] = pydantic.Field(
        alias="parent_id",
    )
    slug: str = pydantic.Field(
        alias="slug",
    )
    """
    the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
    """
    table_of_contents: bool = pydantic.Field(
        alias="table_of_contents",
    )
    children: typing.List["GuideWithChildren"] = pydantic.Field(
        alias="children",
    )
