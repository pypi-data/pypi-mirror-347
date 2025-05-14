import typing

from sideko_portal.core import (
    AsyncBaseClient,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_query_param,
    to_encodable,
)
from sideko_portal.types import models


class AuthClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def exchange_code(
        self, *, code: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.UserApiKey:
        """
        Exchange one-time auth key for api key

        GET /auth/exchange_key

        Args:
            code: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API key

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.auth.exchange_code(code="string")
        ```
        """
        _query: QueryParams = {}
        encode_query_param(
            _query,
            "code",
            to_encodable(item=code, dump_with=str),
            style="form",
            explode=True,
        )
        return self._base_client.request(
            method="GET",
            path="/auth/exchange_key",
            query_params=_query,
            cast_to=models.UserApiKey,
            request_options=request_options or default_request_options(),
        )


class AsyncAuthClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def exchange_code(
        self, *, code: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.UserApiKey:
        """
        Exchange one-time auth key for api key

        GET /auth/exchange_key

        Args:
            code: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API key

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.auth.exchange_code(code="string")
        ```
        """
        _query: QueryParams = {}
        encode_query_param(
            _query,
            "code",
            to_encodable(item=code, dump_with=str),
            style="form",
            explode=True,
        )
        return await self._base_client.request(
            method="GET",
            path="/auth/exchange_key",
            query_params=_query,
            cast_to=models.UserApiKey,
            request_options=request_options or default_request_options(),
        )
