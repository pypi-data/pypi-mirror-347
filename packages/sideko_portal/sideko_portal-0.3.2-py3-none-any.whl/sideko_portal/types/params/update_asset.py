import pydantic
import typing
import typing_extensions


class UpdateAsset(typing_extensions.TypedDict):
    """
    UpdateAsset
    """

    name: typing_extensions.NotRequired[str]
    """
    Asset name (without any extension)
    """


class _SerializerUpdateAsset(pydantic.BaseModel):
    """
    Serializer for UpdateAsset handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
