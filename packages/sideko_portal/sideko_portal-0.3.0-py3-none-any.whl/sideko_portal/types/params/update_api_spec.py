import httpx
import pydantic
import typing
import typing_extensions


class UpdateApiSpec(typing_extensions.TypedDict):
    """
    UpdateApiSpec
    """

    allow_lint_errors: typing_extensions.NotRequired[bool]
    """
    Allow API spec to be updated with a new OpenAPI spec even if it has linting errors
    """

    mock_server_enabled: typing_extensions.NotRequired[bool]
    """
    Enable a public mock server requests for this API Specification
    """

    notes: typing_extensions.NotRequired[str]
    """
    Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
    """

    openapi: typing_extensions.NotRequired[httpx._types.FileTypes]
    """
    An OpenAPI specification in YAML or JSON
    """

    version: typing_extensions.NotRequired[str]
    """
    Semantic Version of the API
    """


class _SerializerUpdateApiSpec(pydantic.BaseModel):
    """
    Serializer for UpdateApiSpec handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    allow_lint_errors: typing.Optional[bool] = pydantic.Field(
        alias="allow_lint_errors", default=None
    )
    mock_server_enabled: typing.Optional[bool] = pydantic.Field(
        alias="mock_server_enabled", default=None
    )
    notes: typing.Optional[str] = pydantic.Field(alias="notes", default=None)
    openapi: typing.Optional[typing.Any] = pydantic.Field(
        alias="openapi", default=None, exclude=True
    )
    version: typing.Optional[str] = pydantic.Field(alias="version", default=None)

    @staticmethod
    def get_files_from_typed_dict(
        item: UpdateApiSpec,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("openapi", None)
        if isinstance(file, list):
            files.extend([("openapi", f) for f in file])
        elif file is not None:
            files.append(("openapi", file))

        return files
