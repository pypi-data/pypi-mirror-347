import typing

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    to_encodable,
    type_utils,
)
from sideko_portal.types import models, params


class DocClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def create(
        self,
        *,
        sdk_id: str,
        modules_filter: typing.Union[
            typing.Optional[typing.List[str]], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.SdkDocResponse:
        """
        Retrieve SDK documentation

        Get documentation for a specific SDK

        POST /sdk/{sdk_id}/doc

        Args:
            modules_filter: Optional array of module names to filter the response
            sdk_id: The SDK ID to get documentation for
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully retrieved SDK documentation

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.sdk.doc.create(sdk_id="h1jasdf123", modules_filter=["user.admin"])
        ```
        """
        _json = to_encodable(
            item={"modules_filter": modules_filter},
            dump_with=params._SerializerSdkDocRequest,
        )
        return self._base_client.request(
            method="POST",
            path=f"/sdk/{sdk_id}/doc",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.SdkDocResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncDocClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def create(
        self,
        *,
        sdk_id: str,
        modules_filter: typing.Union[
            typing.Optional[typing.List[str]], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.SdkDocResponse:
        """
        Retrieve SDK documentation

        Get documentation for a specific SDK

        POST /sdk/{sdk_id}/doc

        Args:
            modules_filter: Optional array of module names to filter the response
            sdk_id: The SDK ID to get documentation for
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully retrieved SDK documentation

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.sdk.doc.create(sdk_id="h1jasdf123", modules_filter=["user.admin"])
        ```
        """
        _json = to_encodable(
            item={"modules_filter": modules_filter},
            dump_with=params._SerializerSdkDocRequest,
        )
        return await self._base_client.request(
            method="POST",
            path=f"/sdk/{sdk_id}/doc",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.SdkDocResponse,
            request_options=request_options or default_request_options(),
        )
