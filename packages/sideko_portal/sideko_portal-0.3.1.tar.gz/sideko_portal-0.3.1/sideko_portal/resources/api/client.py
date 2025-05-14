import httpx
import typing
import typing_extensions

from logging import Logger
from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    filter_not_given,
    to_encodable,
    type_utils,
)
from sideko_portal.resources.api.spec import AsyncSpecClient, SpecClient
from sideko_portal.types import models, params


class ApiClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.spec = SpecClient(base_client=self._base_client)

    def create_and_init_power(
        self,
        *,
        name: str,
        openapi: httpx._types.FileTypes,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiSpec:
        logger = Logger(name="test-logger")
        logger.info("using the new logger yo so we have an import that needs to stay")
        api_res = self.create(name=name)
        return self.spec.create(
            api_name=api_res.name,
            openapi=openapi,
            version="0.1.0",
            mock_server_enabled=True,
            notes="",
        )

    def delete(
        self, *, api_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete an API

        DELETE /api/{api_name}

        Args:
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            API Specification deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.delete(api_name="my-project")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/api/{api_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.Api]:
        """
        List your APIs

        GET /api

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            List of your APIs

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.list()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/api",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.Api],
            request_options=request_options or default_request_options(),
        )

    def get(
        self, *, api_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Api:
        """
        Get one API

        GET /api/{api_name}

        Args:
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an API Specification

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.get(api_name="my-project")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/api/{api_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Api,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        api_name: str,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Api:
        """
        Update an existing API

        PATCH /api/{api_name}

        Args:
            name: str
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            API Specification updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.patch(api_name="my-project", name="my-new-api-name")
        ```
        """
        _json = to_encodable(item={"name": name}, dump_with=params._SerializerUpdateApi)
        return self._base_client.request(
            method="PATCH",
            path=f"/api/{api_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Api,
            request_options=request_options or default_request_options(),
        )

    def create(
        self, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Api:
        """
        Create a new API

        POST /api

        Args:
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.create(name="my-api-spec")
        ```
        """
        _json = to_encodable(item={"name": name}, dump_with=params._SerializerNewApi)
        return self._base_client.request(
            method="POST",
            path="/api",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Api,
            request_options=request_options or default_request_options(),
        )

    def init(
        self,
        *,
        name: str,
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
        Create an API with an initial version

        POST /api/init

        Args:
            allow_lint_errors: Allow API spec to be created even if it has linting errors
            mock_server_enabled: Enable a public mock server requests for this API Specification
            notes: Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
            name: str
            openapi: An OpenAPI specification in YAML or JSON
            version: Semantic version (0.1.0) or a release type (major, minor, patch, rc)
            request_options: Additional options to customize the HTTP request

        Returns:
            API created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api.init(
            name="my-api-spec",
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
                "name": name,
                "openapi": openapi,
                "version": version,
            },
            dump_with=params._SerializerNewApiWithVersion,
        )
        _files = params._SerializerNewApiWithVersion.get_files_from_typed_dict(
            filter_not_given(
                {
                    "allow_lint_errors": allow_lint_errors,
                    "mock_server_enabled": mock_server_enabled,
                    "notes": notes,
                    "name": name,
                    "openapi": openapi,
                    "version": version,
                }
            )
        )
        return self._base_client.request(
            method="POST",
            path="/api/init",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )


class AsyncApiClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.spec = AsyncSpecClient(base_client=self._base_client)

    async def delete(
        self, *, api_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete an API

        DELETE /api/{api_name}

        Args:
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            API Specification deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.delete(api_name="my-project")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/api/{api_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.Api]:
        """
        List your APIs

        GET /api

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            List of your APIs

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.list()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/api",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.Api],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self, *, api_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Api:
        """
        Get one API

        GET /api/{api_name}

        Args:
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an API Specification

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.get(api_name="my-project")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/api/{api_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Api,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        api_name: str,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Api:
        """
        Update an existing API

        PATCH /api/{api_name}

        Args:
            name: str
            api_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            API Specification updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.patch(api_name="my-project", name="my-new-api-name")
        ```
        """
        _json = to_encodable(item={"name": name}, dump_with=params._SerializerUpdateApi)
        return await self._base_client.request(
            method="PATCH",
            path=f"/api/{api_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Api,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Api:
        """
        Create a new API

        POST /api

        Args:
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.create(name="my-api-spec")
        ```
        """
        _json = to_encodable(item={"name": name}, dump_with=params._SerializerNewApi)
        return await self._base_client.request(
            method="POST",
            path="/api",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Api,
            request_options=request_options or default_request_options(),
        )

    async def init(
        self,
        *,
        name: str,
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
        Create an API with an initial version

        POST /api/init

        Args:
            allow_lint_errors: Allow API spec to be created even if it has linting errors
            mock_server_enabled: Enable a public mock server requests for this API Specification
            notes: Text field to add any notes (comments, changelog, etc.) relevant to the version in html format
            name: str
            openapi: An OpenAPI specification in YAML or JSON
            version: Semantic version (0.1.0) or a release type (major, minor, patch, rc)
            request_options: Additional options to customize the HTTP request

        Returns:
            API created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api.init(
            name="my-api-spec",
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
                "name": name,
                "openapi": openapi,
                "version": version,
            },
            dump_with=params._SerializerNewApiWithVersion,
        )
        _files = params._SerializerNewApiWithVersion.get_files_from_typed_dict(
            filter_not_given(
                {
                    "allow_lint_errors": allow_lint_errors,
                    "mock_server_enabled": mock_server_enabled,
                    "notes": notes,
                    "name": name,
                    "openapi": openapi,
                    "version": version,
                }
            )
        )
        return await self._base_client.request(
            method="POST",
            path="/api/init",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.ApiSpec,
            request_options=request_options or default_request_options(),
        )
