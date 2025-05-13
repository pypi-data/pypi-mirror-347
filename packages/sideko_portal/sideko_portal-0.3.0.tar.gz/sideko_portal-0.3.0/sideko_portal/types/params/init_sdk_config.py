import pydantic
import typing
import typing_extensions


class InitSdkConfig(typing_extensions.TypedDict):
    """
    InitSdkConfig
    """

    api_name: typing_extensions.Required[str]
    """
    Unique project name or the uuid
    """

    api_version: typing_extensions.NotRequired[
        typing.Union[typing_extensions.Literal["latest"], str]
    ]
    """
    Can be either the semantic version or a released type (like latest)
    """

    default_module_structure: typing_extensions.NotRequired[
        typing_extensions.Literal["flat", "path", "tag"]
    ]
    """
    Configures the default algorithm which determines modules and function names for the SDK
    """


class _SerializerInitSdkConfig(pydantic.BaseModel):
    """
    Serializer for InitSdkConfig handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_name: str = pydantic.Field(
        alias="api_name",
    )
    api_version: typing.Optional[
        typing.Union[typing_extensions.Literal["latest"], str]
    ] = pydantic.Field(alias="api_version", default=None)
    default_module_structure: typing.Optional[
        typing_extensions.Literal["flat", "path", "tag"]
    ] = pydantic.Field(alias="default_module_structure", default=None)
