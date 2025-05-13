import httpx
import pydantic
import typing
import typing_extensions


class UpdateSdk(typing_extensions.TypedDict):
    """
    UpdateSdk
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

    prev_sdk_git: typing_extensions.Required[httpx._types.FileTypes]
    """
    compressed .tar.gz of .git/ directory of previous SDK
    """

    prev_sdk_id: typing_extensions.Required[str]

    sdk_version: typing_extensions.Required[
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


class _SerializerUpdateSdk(pydantic.BaseModel):
    """
    Serializer for UpdateSdk handling case conversions
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
    prev_sdk_git: typing.Optional[typing.Any] = pydantic.Field(
        alias="prev_sdk_git", default=None, exclude=True
    )
    prev_sdk_id: str = pydantic.Field(
        alias="prev_sdk_id",
    )
    sdk_version: typing.Union[
        typing_extensions.Literal[
            "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
        ],
        str,
    ] = pydantic.Field(
        alias="sdk_version",
    )

    @staticmethod
    def get_files_from_typed_dict(
        item: UpdateSdk,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("config", None)
        if isinstance(file, list):
            files.extend([("config", f) for f in file])
        elif file is not None:
            files.append(("config", file))

        file = item.get("prev_sdk_git", None)
        if isinstance(file, list):
            files.extend([("prev_sdk_git", f) for f in file])
        elif file is not None:
            files.append(("prev_sdk_git", file))

        return files
