import httpx
import typing
import typing_extensions

from sideko_portal.core import (
    AsyncBaseClient,
    BinaryResponse,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_query_param,
    filter_not_given,
    to_encodable,
    type_utils,
)
from sideko_portal.resources.sdk.config import AsyncConfigClient, ConfigClient
from sideko_portal.resources.sdk.doc import AsyncDocClient, DocClient
from sideko_portal.types import models, params


class SdkClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.config = ConfigClient(base_client=self._base_client)
        self.doc = DocClient(base_client=self._base_client)

    def list(
        self,
        *,
        api_name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        successful: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.SdkGeneration]:
        """
        List all managed SDKs

        GET /sdk

        Args:
            api_name: Filter by API name or ID (uuid)
            successful: Filter by SDK generation success
            request_options: Additional options to customize the HTTP request

        Returns:
            SDK generations matching query

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.sdk.list()
        ```
        """
        _query: QueryParams = {}
        if not isinstance(api_name, type_utils.NotGiven):
            encode_query_param(
                _query,
                "api_name",
                to_encodable(item=api_name, dump_with=str),
                style="form",
                explode=True,
            )
        if not isinstance(successful, type_utils.NotGiven):
            encode_query_param(
                _query,
                "successful",
                to_encodable(item=successful, dump_with=bool),
                style="form",
                explode=True,
            )
        return self._base_client.request(
            method="GET",
            path="/sdk",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.SdkGeneration],
            request_options=request_options or default_request_options(),
        )

    def generate(
        self,
        *,
        config: httpx._types.FileTypes,
        language: typing_extensions.Literal[
            "go", "java", "python", "rust", "typescript"
        ],
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        github_actions: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        sdk_version: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BinaryResponse:
        """
        Generate a new managed SDK from a Sideko configuration file

        POST /sdk

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            github_actions: include github action boilerplate for running tests and publishing the sdk
            sdk_version: Semantic version following conventions from https://semver.org/
            config: SDK configuration file in .yaml format
            language: Programming languages available for SDK generation
            request_options: Additional options to customize the HTTP request

        Returns:
            Generated sdk codebase compressed as .tar.gz

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.sdk.generate(
            config=open("uploads/config.yaml", "rb"), language="go", sdk_version="0.1.0"
        )
        ```
        """
        _data = to_encodable(
            item={
                "api_version": api_version,
                "github_actions": github_actions,
                "sdk_version": sdk_version,
                "config": config,
                "language": language,
            },
            dump_with=params._SerializerNewSdk,
        )
        _files = params._SerializerNewSdk.get_files_from_typed_dict(
            filter_not_given(
                {
                    "api_version": api_version,
                    "github_actions": github_actions,
                    "sdk_version": sdk_version,
                    "config": config,
                    "language": language,
                }
            )
        )
        return self._base_client.request(
            method="POST",
            path="/sdk",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=BinaryResponse,
            request_options=request_options or default_request_options(),
        )

    def update(
        self,
        *,
        config: httpx._types.FileTypes,
        prev_sdk_git: httpx._types.FileTypes,
        prev_sdk_id: str,
        sdk_version: typing.Union[
            typing_extensions.Literal[
                "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
            ],
            str,
        ],
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> str:
        """
        Update an SDK to reflect the latest state of the API

        POST /sdk/update

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            config: SDK configuration file in .yaml format
            prev_sdk_git: compressed .tar.gz of .git/ directory of previous SDK
            prev_sdk_id: str
            sdk_version: Semantic version (0.1.0) or a release type (major, minor, patch, rc)
            request_options: Additional options to customize the HTTP request

        Returns:
            Generate a git patch file to update your SDK. The response is a text file.

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.sdk.update(
            config=open("uploads/config.yaml", "rb"),
            prev_sdk_git=open("uploads/git.tar.gz", "rb"),
            prev_sdk_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            sdk_version="major",
        )
        ```
        """
        _data = to_encodable(
            item={
                "api_version": api_version,
                "config": config,
                "prev_sdk_git": prev_sdk_git,
                "prev_sdk_id": prev_sdk_id,
                "sdk_version": sdk_version,
            },
            dump_with=params._SerializerUpdateSdk,
        )
        _files = params._SerializerUpdateSdk.get_files_from_typed_dict(
            filter_not_given(
                {
                    "api_version": api_version,
                    "config": config,
                    "prev_sdk_git": prev_sdk_git,
                    "prev_sdk_id": prev_sdk_id,
                    "sdk_version": sdk_version,
                }
            )
        )
        return self._base_client.request(
            method="POST",
            path="/sdk/update",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=str,
            request_options=request_options or default_request_options(),
        )


class AsyncSdkClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.config = AsyncConfigClient(base_client=self._base_client)
        self.doc = AsyncDocClient(base_client=self._base_client)

    async def list(
        self,
        *,
        api_name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        successful: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.SdkGeneration]:
        """
        List all managed SDKs

        GET /sdk

        Args:
            api_name: Filter by API name or ID (uuid)
            successful: Filter by SDK generation success
            request_options: Additional options to customize the HTTP request

        Returns:
            SDK generations matching query

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.sdk.list()
        ```
        """
        _query: QueryParams = {}
        if not isinstance(api_name, type_utils.NotGiven):
            encode_query_param(
                _query,
                "api_name",
                to_encodable(item=api_name, dump_with=str),
                style="form",
                explode=True,
            )
        if not isinstance(successful, type_utils.NotGiven):
            encode_query_param(
                _query,
                "successful",
                to_encodable(item=successful, dump_with=bool),
                style="form",
                explode=True,
            )
        return await self._base_client.request(
            method="GET",
            path="/sdk",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.SdkGeneration],
            request_options=request_options or default_request_options(),
        )

    async def generate(
        self,
        *,
        config: httpx._types.FileTypes,
        language: typing_extensions.Literal[
            "go", "java", "python", "rust", "typescript"
        ],
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        github_actions: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        sdk_version: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BinaryResponse:
        """
        Generate a new managed SDK from a Sideko configuration file

        POST /sdk

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            github_actions: include github action boilerplate for running tests and publishing the sdk
            sdk_version: Semantic version following conventions from https://semver.org/
            config: SDK configuration file in .yaml format
            language: Programming languages available for SDK generation
            request_options: Additional options to customize the HTTP request

        Returns:
            Generated sdk codebase compressed as .tar.gz

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.sdk.generate(
            config=open("uploads/config.yaml", "rb"), language="go", sdk_version="0.1.0"
        )
        ```
        """
        _data = to_encodable(
            item={
                "api_version": api_version,
                "github_actions": github_actions,
                "sdk_version": sdk_version,
                "config": config,
                "language": language,
            },
            dump_with=params._SerializerNewSdk,
        )
        _files = params._SerializerNewSdk.get_files_from_typed_dict(
            filter_not_given(
                {
                    "api_version": api_version,
                    "github_actions": github_actions,
                    "sdk_version": sdk_version,
                    "config": config,
                    "language": language,
                }
            )
        )
        return await self._base_client.request(
            method="POST",
            path="/sdk",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=BinaryResponse,
            request_options=request_options or default_request_options(),
        )

    async def update(
        self,
        *,
        config: httpx._types.FileTypes,
        prev_sdk_git: httpx._types.FileTypes,
        prev_sdk_id: str,
        sdk_version: typing.Union[
            typing_extensions.Literal[
                "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
            ],
            str,
        ],
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> str:
        """
        Update an SDK to reflect the latest state of the API

        POST /sdk/update

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            config: SDK configuration file in .yaml format
            prev_sdk_git: compressed .tar.gz of .git/ directory of previous SDK
            prev_sdk_id: str
            sdk_version: Semantic version (0.1.0) or a release type (major, minor, patch, rc)
            request_options: Additional options to customize the HTTP request

        Returns:
            Generate a git patch file to update your SDK. The response is a text file.

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.sdk.update(
            config=open("uploads/config.yaml", "rb"),
            prev_sdk_git=open("uploads/git.tar.gz", "rb"),
            prev_sdk_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            sdk_version="major",
        )
        ```
        """
        _data = to_encodable(
            item={
                "api_version": api_version,
                "config": config,
                "prev_sdk_git": prev_sdk_git,
                "prev_sdk_id": prev_sdk_id,
                "sdk_version": sdk_version,
            },
            dump_with=params._SerializerUpdateSdk,
        )
        _files = params._SerializerUpdateSdk.get_files_from_typed_dict(
            filter_not_given(
                {
                    "api_version": api_version,
                    "config": config,
                    "prev_sdk_git": prev_sdk_git,
                    "prev_sdk_id": prev_sdk_id,
                    "sdk_version": sdk_version,
                }
            )
        )
        return await self._base_client.request(
            method="POST",
            path="/sdk/update",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=str,
            request_options=request_options or default_request_options(),
        )
