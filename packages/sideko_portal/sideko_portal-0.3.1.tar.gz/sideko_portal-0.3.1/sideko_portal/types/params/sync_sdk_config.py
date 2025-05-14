import httpx
import pydantic
import typing
import typing_extensions


class SyncSdkConfig(typing_extensions.TypedDict):
    """
    SyncSdkConfig
    """

    api_version: typing_extensions.NotRequired[
        typing.Union[typing_extensions.Literal["latest"], str]
    ]
    """
    Can be either the semantic version or a released type (like latest)
    """

    config: typing_extensions.Required[httpx._types.FileTypes]
    """
    SDK configuration file in .yaml format
    """

    openapi: typing_extensions.NotRequired[httpx._types.FileTypes]
    """
    Use api_version in typical use. If this field is supplied, the configuration sync will match the spec rather than any API that lives in Sideko.
    """


class _SerializerSyncSdkConfig(pydantic.BaseModel):
    """
    Serializer for SyncSdkConfig handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_version: typing.Optional[
        typing.Union[typing_extensions.Literal["latest"], str]
    ] = pydantic.Field(alias="api_version", default=None)
    config: typing.Optional[typing.Any] = pydantic.Field(
        alias="config", default=None, exclude=True
    )
    openapi: typing.Optional[typing.Any] = pydantic.Field(
        alias="openapi", default=None, exclude=True
    )

    @staticmethod
    def get_files_from_typed_dict(
        item: SyncSdkConfig,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("config", None)
        if isinstance(file, list):
            files.extend([("config", f) for f in file])
        elif file is not None:
            files.append(("config", file))

        file = item.get("openapi", None)
        if isinstance(file, list):
            files.extend([("openapi", f) for f in file])
        elif file is not None:
            files.append(("openapi", file))

        return files
