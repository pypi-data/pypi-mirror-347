import httpx
import typing
import typing_extensions

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    filter_not_given,
    to_encodable,
    type_utils,
)
from sideko_portal.types import models, params


class SpecClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete an API Specification and it's associated metadata

        DELETE /api/{api_name}/spec/{api_version}

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            Successful deletion

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.delete(api_name="my-project", api_version="latest")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/api/{api_name}/spec/{api_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self, *, api_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.ApiSpec]:
        """
        List specs of a collection

        GET /api/{api_name}/spec

        Args:
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            List of API Specs for a given collection

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.list(api_name="my-project")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.ApiSpec],
            request_options=request_options or default_request_options(),
        )

    def get(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        """
        Get API specification metadata

        GET /api/{api_name}/spec/{api_version}

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an API Specification version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.get(api_name="my-project", api_version="latest")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec/{api_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )

    def get_openapi(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.OpenApi:
        """
        Get OpenAPI specification

        GET /api/{api_name}/spec/{api_version}/openapi

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            OpenAPI Specification as JSON and OAS metadata

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.get_openapi(api_name="my-project", api_version="latest")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec/{api_version}/openapi",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.OpenApi,
            request_options=request_options or default_request_options(),
        )

    def get_stats(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpecStats:
        """
        Get Stats about the specification

        GET /api/{api_name}/spec/{api_version}/stats

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            OpenAPI Stats Data

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.get_stats(api_name="my-project", api_version="latest")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec/{api_version}/stats",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.ApiSpecStats,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        allow_lint_errors: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mock_server_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        notes: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        openapi: typing.Union[
            typing.Optional[httpx._types.FileTypes], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        version: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        """
        Update an API Specification and/or metadata

        PATCH /api/{api_name}/spec/{api_version}

        Args:
            allow_lint_errors: Allow API spec to be updated with a new OpenAPI spec even if it has linting errors
            mock_server_enabled: Enable a public mock server requests for this API Specification
            notes: Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
            openapi: An OpenAPI specification in YAML or JSON
            version: Semantic Version of the API
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an API Specification version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.patch(
            api_name="my-project",
            api_version="latest",
            notes="<p>This version includes a number of excellent improvements</p>",
            openapi=open("uploads/openapi.yaml", "rb"),
        )
        ```
        """
        _data = to_encodable(
            item={
                "allow_lint_errors": allow_lint_errors,
                "mock_server_enabled": mock_server_enabled,
                "notes": notes,
                "openapi": openapi,
                "version": version,
            },
            dump_with=params._SerializerUpdateApiSpec,
        )
        _files = params._SerializerUpdateApiSpec.get_files_from_typed_dict(
            filter_not_given(
                {
                    "allow_lint_errors": allow_lint_errors,
                    "mock_server_enabled": mock_server_enabled,
                    "notes": notes,
                    "openapi": openapi,
                    "version": version,
                }
            )
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/api/{api_name}/spec/{api_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        api_name: str,
        openapi: httpx._types.FileTypes,
        version: typing.Union[
            typing_extensions.Literal[
                "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
            ],
            str,
        ],
        allow_lint_errors: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mock_server_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        notes: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        """
        Add a new API specification

        POST /api/{api_name}/spec

        Args:
            allow_lint_errors: Allow API spec to be created even if it has linting errors
            mock_server_enabled: Enable a public mock server requests for this API Specification
            notes: Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
            api_name: Unique project name or the uuid
            openapi: An OpenAPI specification in YAML or JSON
            version: Semantic version (0.1.0) or a release type (major, minor, patch, rc)
            request_options: Additional options to customize the HTTP request

        Returns:
            Version created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.spec.create(
            api_name="my-project",
            openapi=open("uploads/openapi.yaml", "rb"),
            version="major",
            notes="<p>This version includes a number of excellent improvements</p>",
        )
        ```
        """
        _data = to_encodable(
            item={
                "allow_lint_errors": allow_lint_errors,
                "mock_server_enabled": mock_server_enabled,
                "notes": notes,
                "openapi": openapi,
                "version": version,
            },
            dump_with=params._SerializerNewApiSpec,
        )
        _files = params._SerializerNewApiSpec.get_files_from_typed_dict(
            filter_not_given(
                {
                    "allow_lint_errors": allow_lint_errors,
                    "mock_server_enabled": mock_server_enabled,
                    "notes": notes,
                    "openapi": openapi,
                    "version": version,
                }
            )
        )
        return self._base_client.request(
            method="POST",
            path=f"/api/{api_name}/spec",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )


class AsyncSpecClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete an API Specification and it's associated metadata

        DELETE /api/{api_name}/spec/{api_version}

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            Successful deletion

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.delete(api_name="my-project", api_version="latest")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/api/{api_name}/spec/{api_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self, *, api_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.ApiSpec]:
        """
        List specs of a collection

        GET /api/{api_name}/spec

        Args:
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            List of API Specs for a given collection

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.list(api_name="my-project")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.ApiSpec],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        """
        Get API specification metadata

        GET /api/{api_name}/spec/{api_version}

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an API Specification version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.get(api_name="my-project", api_version="latest")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec/{api_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )

    async def get_openapi(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.OpenApi:
        """
        Get OpenAPI specification

        GET /api/{api_name}/spec/{api_version}/openapi

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            OpenAPI Specification as JSON and OAS metadata

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.get_openapi(api_name="my-project", api_version="latest")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec/{api_version}/openapi",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.OpenApi,
            request_options=request_options or default_request_options(),
        )

    async def get_stats(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpecStats:
        """
        Get Stats about the specification

        GET /api/{api_name}/spec/{api_version}/stats

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            OpenAPI Stats Data

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.get_stats(api_name="my-project", api_version="latest")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/api/{api_name}/spec/{api_version}/stats",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.ApiSpecStats,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        api_name: str,
        api_version: typing.Union[typing_extensions.Literal["latest"], str],
        allow_lint_errors: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mock_server_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        notes: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        openapi: typing.Union[
            typing.Optional[httpx._types.FileTypes], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        version: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        """
        Update an API Specification and/or metadata

        PATCH /api/{api_name}/spec/{api_version}

        Args:
            allow_lint_errors: Allow API spec to be updated with a new OpenAPI spec even if it has linting errors
            mock_server_enabled: Enable a public mock server requests for this API Specification
            notes: Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
            openapi: An OpenAPI specification in YAML or JSON
            version: Semantic Version of the API
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an API Specification version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.patch(
            api_name="my-project",
            api_version="latest",
            notes="<p>This version includes a number of excellent improvements</p>",
            openapi=open("uploads/openapi.yaml", "rb"),
        )
        ```
        """
        _data = to_encodable(
            item={
                "allow_lint_errors": allow_lint_errors,
                "mock_server_enabled": mock_server_enabled,
                "notes": notes,
                "openapi": openapi,
                "version": version,
            },
            dump_with=params._SerializerUpdateApiSpec,
        )
        _files = params._SerializerUpdateApiSpec.get_files_from_typed_dict(
            filter_not_given(
                {
                    "allow_lint_errors": allow_lint_errors,
                    "mock_server_enabled": mock_server_enabled,
                    "notes": notes,
                    "openapi": openapi,
                    "version": version,
                }
            )
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/api/{api_name}/spec/{api_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        api_name: str,
        openapi: httpx._types.FileTypes,
        version: typing.Union[
            typing_extensions.Literal[
                "major", "minor", "patch", "rc", "rc-major", "rc-minor", "rc-patch"
            ],
            str,
        ],
        allow_lint_errors: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        mock_server_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        notes: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        """
        Add a new API specification

        POST /api/{api_name}/spec

        Args:
            allow_lint_errors: Allow API spec to be created even if it has linting errors
            mock_server_enabled: Enable a public mock server requests for this API Specification
            notes: Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
            api_name: Unique project name or the uuid
            openapi: An OpenAPI specification in YAML or JSON
            version: Semantic version (0.1.0) or a release type (major, minor, patch, rc)
            request_options: Additional options to customize the HTTP request

        Returns:
            Version created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.spec.create(
            api_name="my-project",
            openapi=open("uploads/openapi.yaml", "rb"),
            version="major",
            notes="<p>This version includes a number of excellent improvements</p>",
        )
        ```
        """
        _data = to_encodable(
            item={
                "allow_lint_errors": allow_lint_errors,
                "mock_server_enabled": mock_server_enabled,
                "notes": notes,
                "openapi": openapi,
                "version": version,
            },
            dump_with=params._SerializerNewApiSpec,
        )
        _files = params._SerializerNewApiSpec.get_files_from_typed_dict(
            filter_not_given(
                {
                    "allow_lint_errors": allow_lint_errors,
                    "mock_server_enabled": mock_server_enabled,
                    "notes": notes,
                    "openapi": openapi,
                    "version": version,
                }
            )
        )
        return await self._base_client.request(
            method="POST",
            path=f"/api/{api_name}/spec",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )
