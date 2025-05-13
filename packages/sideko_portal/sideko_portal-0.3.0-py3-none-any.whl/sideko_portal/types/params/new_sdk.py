import httpx
import pydantic
import typing
import typing_extensions


class NewSdk(typing_extensions.TypedDict):
    """
    NewSdk
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

    github_actions: typing_extensions.NotRequired[bool]
    """
    include github action boilerplate for running tests and publishing the sdk
    """

    language: typing_extensions.Required[
        typing_extensions.Literal["go", "java", "python", "rust", "typescript"]
    ]
    """
    Programming languages available for SDK generation
    """

    sdk_version: typing_extensions.NotRequired[str]
    """
    Semantic version following conventions from https://semver.org/
    """


class _SerializerNewSdk(pydantic.BaseModel):
    """
    Serializer for NewSdk handling case conversions
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
    github_actions: typing.Optional[bool] = pydantic.Field(
        alias="github_actions", default=None
    )
    language: typing_extensions.Literal[
        "go", "java", "python", "rust", "typescript"
    ] = pydantic.Field(
        alias="language",
    )
    sdk_version: typing.Optional[str] = pydantic.Field(
        alias="sdk_version", default=None
    )

    @staticmethod
    def get_files_from_typed_dict(
        item: NewSdk,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("config", None)
        if isinstance(file, list):
            files.extend([("config", f) for f in file])
        elif file is not None:
            files.append(("config", file))

        return files
