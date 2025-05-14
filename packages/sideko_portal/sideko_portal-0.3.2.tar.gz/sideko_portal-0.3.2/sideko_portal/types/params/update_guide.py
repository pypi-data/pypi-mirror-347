import pydantic
import typing
import typing_extensions


class UpdateGuide(typing_extensions.TypedDict):
    """
    UpdateGuide
    """

    content: typing_extensions.NotRequired[str]

    icon: typing_extensions.NotRequired[typing.Optional[str]]
    """
    lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
    """

    nav_label: typing_extensions.NotRequired[str]
    """
    the label that shows on the navbar for this guide
    """

    next_id: typing_extensions.NotRequired[typing.Optional[str]]

    prev_id: typing_extensions.NotRequired[typing.Optional[str]]

    slug: typing_extensions.NotRequired[str]
    """
    the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
    """

    table_of_contents: typing_extensions.NotRequired[bool]


class _SerializerUpdateGuide(pydantic.BaseModel):
    """
    Serializer for UpdateGuide handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    content: typing.Optional[str] = pydantic.Field(alias="content", default=None)
    icon: typing.Optional[str] = pydantic.Field(alias="icon", default=None)
    nav_label: typing.Optional[str] = pydantic.Field(alias="nav_label", default=None)
    next_id: typing.Optional[str] = pydantic.Field(alias="next_id", default=None)
    prev_id: typing.Optional[str] = pydantic.Field(alias="prev_id", default=None)
    slug: typing.Optional[str] = pydantic.Field(alias="slug", default=None)
    table_of_contents: typing.Optional[bool] = pydantic.Field(
        alias="table_of_contents", default=None
    )
