import pydantic
import typing_extensions


class DocPreviewPasswordName(typing_extensions.TypedDict):
    """
    DocPreviewPasswordName
    """

    name: typing_extensions.Required[str]


class _SerializerDocPreviewPasswordName(pydantic.BaseModel):
    """
    Serializer for DocPreviewPasswordName handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: str = pydantic.Field(
        alias="name",
    )
