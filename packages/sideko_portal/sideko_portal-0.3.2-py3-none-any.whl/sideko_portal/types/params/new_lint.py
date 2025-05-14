import httpx
import pydantic
import typing
import typing_extensions


class NewLint(typing_extensions.TypedDict):
    """
    You must either provide `openapi` OR (`api_name` AND `api_version`)
    """

    api_name: typing_extensions.NotRequired[str]
    """
    Unique project name or the uuid
    """

    api_version: typing_extensions.NotRequired[
        typing.Union[typing_extensions.Literal["latest"], str]
    ]
    """
    Can be either the semantic version or a released type (like latest)
    """

    openapi: typing_extensions.NotRequired[httpx._types.FileTypes]


class _SerializerNewLint(pydantic.BaseModel):
    """
    Serializer for NewLint handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    api_name: typing.Optional[str] = pydantic.Field(alias="api_name", default=None)
    api_version: typing.Optional[
        typing.Union[typing_extensions.Literal["latest"], str]
    ] = pydantic.Field(alias="api_version", default=None)
    openapi: typing.Optional[typing.Any] = pydantic.Field(
        alias="openapi", default=None, exclude=True
    )

    @staticmethod
    def get_files_from_typed_dict(
        item: NewLint,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("openapi", None)
        if isinstance(file, list):
            files.extend([("openapi", f) for f in file])
        elif file is not None:
            files.append(("openapi", file))

        return files
