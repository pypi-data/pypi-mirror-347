import pydantic
import typing
import typing_extensions


class SdkDocRequest(typing_extensions.TypedDict):
    """
    SdkDocRequest
    """

    modules_filter: typing_extensions.NotRequired[typing.List[str]]
    """
    Optional array of module names to filter the response
    """


class _SerializerSdkDocRequest(pydantic.BaseModel):
    """
    Serializer for SdkDocRequest handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    modules_filter: typing.Optional[typing.List[str]] = pydantic.Field(
        alias="modules_filter", default=None
    )
