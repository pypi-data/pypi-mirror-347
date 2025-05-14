import pydantic
import typing
import typing_extensions


class NewGuide(typing_extensions.TypedDict):
    """
    NewGuide
    """

    content: typing_extensions.Required[str]

    icon: typing_extensions.NotRequired[str]
    """
    lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
    """

    is_parent: typing_extensions.Required[bool]

    nav_label: typing_extensions.Required[str]
    """
    the label that shows on the navbar for this guide
    """

    next_id: typing_extensions.NotRequired[str]

    parent_id: typing_extensions.NotRequired[str]

    prev_id: typing_extensions.NotRequired[str]

    slug: typing_extensions.Required[str]
    """
    the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
    """

    table_of_contents: typing_extensions.NotRequired[bool]


class _SerializerNewGuide(pydantic.BaseModel):
    """
    Serializer for NewGuide handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    content: str = pydantic.Field(
        alias="content",
    )
    icon: typing.Optional[str] = pydantic.Field(alias="icon", default=None)
    is_parent: bool = pydantic.Field(
        alias="is_parent",
    )
    nav_label: str = pydantic.Field(
        alias="nav_label",
    )
    next_id: typing.Optional[str] = pydantic.Field(alias="next_id", default=None)
    parent_id: typing.Optional[str] = pydantic.Field(alias="parent_id", default=None)
    prev_id: typing.Optional[str] = pydantic.Field(alias="prev_id", default=None)
    slug: str = pydantic.Field(
        alias="slug",
    )
    table_of_contents: typing.Optional[bool] = pydantic.Field(
        alias="table_of_contents", default=None
    )
