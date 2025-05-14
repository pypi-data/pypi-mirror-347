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


class LintClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def run(
        self,
        *,
        api_name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        openapi: typing.Union[
            typing.Optional[httpx._types.FileTypes], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.LintReport:
        """
        Lint an OpenAPI spec

        POST /lint

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            openapi: httpx._types.FileTypes
            request_options: Additional options to customize the HTTP request

        Returns:
            Linting report

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.lint.run(
            api_name="my-project", openapi=open("uploads/openapi.yaml", "rb")
        )
        ```
        """
        _data = to_encodable(
            item={"api_name": api_name, "api_version": api_version, "openapi": openapi},
            dump_with=params._SerializerNewLint,
        )
        _files = params._SerializerNewLint.get_files_from_typed_dict(
            filter_not_given(
                {"api_name": api_name, "api_version": api_version, "openapi": openapi}
            )
        )
        return self._base_client.request(
            method="POST",
            path="/lint",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.LintReport,
            request_options=request_options or default_request_options(),
        )


class AsyncLintClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def run(
        self,
        *,
        api_name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        api_version: typing.Union[
            typing.Optional[typing.Union[typing_extensions.Literal["latest"], str]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        openapi: typing.Union[
            typing.Optional[httpx._types.FileTypes], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.LintReport:
        """
        Lint an OpenAPI spec

        POST /lint

        Args:
            api_name: Unique project name or the uuid
            api_version: Can be either the semantic version or a released type (like latest)
            openapi: httpx._types.FileTypes
            request_options: Additional options to customize the HTTP request

        Returns:
            Linting report

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.lint.run(
            api_name="my-project", openapi=open("uploads/openapi.yaml", "rb")
        )
        ```
        """
        _data = to_encodable(
            item={"api_name": api_name, "api_version": api_version, "openapi": openapi},
            dump_with=params._SerializerNewLint,
        )
        _files = params._SerializerNewLint.get_files_from_typed_dict(
            filter_not_given(
                {"api_name": api_name, "api_version": api_version, "openapi": openapi}
            )
        )
        return await self._base_client.request(
            method="POST",
            path="/lint",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=models.LintReport,
            request_options=request_options or default_request_options(),
        )
