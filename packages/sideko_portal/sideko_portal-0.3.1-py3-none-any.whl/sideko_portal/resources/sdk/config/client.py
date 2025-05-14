import httpx
import typing
import typing_extensions

from sideko_portal.core import (
    AsyncBaseClient,
    BinaryResponse,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    filter_not_given,
    to_encodable,
    type_utils,
)
from sideko_portal.types import params


class ConfigClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def init(
        self,
        *,
        api_name: str,
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        default_module_structure: typing.Union[
            typing.Optional[typing_extensions.Literal["flat", "path", "tag"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BinaryResponse:
        """
        Initialize an SDK configuration with all defaults applied

        Creates a sdk config with default configurations for the api/api version

        POST /sdk/config/init

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            default_module_structure: Configures the default algorithm which determines modules and function names for the SDK
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            New SDK configuration in .yaml format

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.sdk.config.init(api_name="my-project")
        ```
        """
        _json = to_encodable(
            item={
                "api_version": api_version,
                "default_module_structure": default_module_structure,
                "api_name": api_name,
            },
            dump_with=params._SerializerInitSdkConfig,
        )
        return self._base_client.request(
            method="POST",
            path="/sdk/config/init",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=BinaryResponse,
            request_options=request_options or default_request_options(),
        )

    def sync(
        self,
        *,
        config: httpx._types.FileTypes,
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        openapi: typing.Union[
            typing.Optional[httpx._types.FileTypes], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BinaryResponse:
        """
        Sync an SDK configuration with the latest state of the API

        Updates provided config with missing default configurations for the api version

        POST /sdk/config/sync

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            openapi: Use api_version in typical use. If this field is supplied, the configuration sync will match the spec rather than any API that lives in Sideko.
            config: SDK configuration file in .yaml format
            request_options: Additional options to customize the HTTP request

        Returns:
            New SDK configuration in .yaml format

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.sdk.config.sync(
            config=open("uploads/config.yaml", "rb"),
            openapi=open("uploads/openapi.yaml", "rb"),
        )
        ```
        """
        _data = to_encodable(
            item={"api_version": api_version, "openapi": openapi, "config": config},
            dump_with=params._SerializerSyncSdkConfig,
        )
        _files = params._SerializerSyncSdkConfig.get_files_from_typed_dict(
            filter_not_given(
                {"api_version": api_version, "openapi": openapi, "config": config}
            )
        )
        return self._base_client.request(
            method="POST",
            path="/sdk/config/sync",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=BinaryResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncConfigClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def init(
        self,
        *,
        api_name: str,
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        default_module_structure: typing.Union[
            typing.Optional[typing_extensions.Literal["flat", "path", "tag"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BinaryResponse:
        """
        Initialize an SDK configuration with all defaults applied

        Creates a sdk config with default configurations for the api/api version

        POST /sdk/config/init

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            default_module_structure: Configures the default algorithm which determines modules and function names for the SDK
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            New SDK configuration in .yaml format

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.sdk.config.init(api_name="my-project")
        ```
        """
        _json = to_encodable(
            item={
                "api_version": api_version,
                "default_module_structure": default_module_structure,
                "api_name": api_name,
            },
            dump_with=params._SerializerInitSdkConfig,
        )
        return await self._base_client.request(
            method="POST",
            path="/sdk/config/init",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=BinaryResponse,
            request_options=request_options or default_request_options(),
        )

    async def sync(
        self,
        *,
        config: httpx._types.FileTypes,
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        openapi: typing.Union[
            typing.Optional[httpx._types.FileTypes], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BinaryResponse:
        """
        Sync an SDK configuration with the latest state of the API

        Updates provided config with missing default configurations for the api version

        POST /sdk/config/sync

        Args:
            api_version: Can be either the semantic version or a released type (like latest)
            openapi: Use api_version in typical use. If this field is supplied, the configuration sync will match the spec rather than any API that lives in Sideko.
            config: SDK configuration file in .yaml format
            request_options: Additional options to customize the HTTP request

        Returns:
            New SDK configuration in .yaml format

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.sdk.config.sync(
            config=open("uploads/config.yaml", "rb"),
            openapi=open("uploads/openapi.yaml", "rb"),
        )
        ```
        """
        _data = to_encodable(
            item={"api_version": api_version, "openapi": openapi, "config": config},
            dump_with=params._SerializerSyncSdkConfig,
        )
        _files = params._SerializerSyncSdkConfig.get_files_from_typed_dict(
            filter_not_given(
                {"api_version": api_version, "openapi": openapi, "config": config}
            )
        )
        return await self._base_client.request(
            method="POST",
            path="/sdk/config/sync",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=BinaryResponse,
            request_options=request_options or default_request_options(),
        )
