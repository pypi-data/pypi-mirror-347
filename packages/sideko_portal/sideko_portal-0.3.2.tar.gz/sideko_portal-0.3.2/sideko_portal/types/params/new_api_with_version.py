import httpx
import pydantic
import typing
import typing_extensions


class NewApiWithVersion(typing_extensions.TypedDict):
    """
    NewApiWithVersion
    """

    name: typing_extensions.Required[str]

    allow_lint_errors: typing_extensions.NotRequired[bool]
    """
    Allow API spec to be created even if it has linting errors
    """

    mock_server_enabled: typing_extensions.NotRequired[bool]
    """
    Enable a public mock server requests for this API Specification
    """

    notes: typing_extensions.NotRequired[str]
    """
    Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
    """

    openapi: typing_extensions.Required[httpx._types.FileTypes]
    """
    An OpenAPI specification in YAML or JSON
    """

    version: typing_extensions.Required[
        typing.Union[
            typing_extensions.Literal[
                "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
            ],
            str,
        ]
    ]
    """
    Semantic version (0.1.0) or a release type (major, minor, patch, rc)
    """


class _SerializerNewApiWithVersion(pydantic.BaseModel):
    """
    Serializer for NewApiWithVersion handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    name: str = pydantic.Field(
        alias="name",
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
    version: typing.Union[
        typing_extensions.Literal[
            "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
        ],
        str,
    ] = pydantic.Field(
        alias="version",
    )

    @staticmethod
    def get_files_from_typed_dict(
        item: NewApiWithVersion,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("openapi", None)
        if isinstance(file, list):
            files.extend([("openapi", f) for f in file])
        elif file is not None:
            files.append(("openapi", file))

        return files
