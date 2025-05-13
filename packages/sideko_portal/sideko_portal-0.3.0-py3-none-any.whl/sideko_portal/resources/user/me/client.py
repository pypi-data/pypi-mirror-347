import typing

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
)
from sideko_portal.types import models


class MeClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.User:
        """
        Get current user profile

        GET /user/me

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            User profile

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.user.me.get()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/user/me",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.User,
            request_options=request_options or default_request_options(),
        )

    def get_key(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.UserApiKey:
        """
        Get API key for the current user

        GET /user/me/api_key

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            API key

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.user.me.get_key()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/user/me/api_key",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.UserApiKey,
            request_options=request_options or default_request_options(),
        )


class AsyncMeClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.User:
        """
        Get current user profile

        GET /user/me

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            User profile

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.user.me.get()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/user/me",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.User,
            request_options=request_options or default_request_options(),
        )

    async def get_key(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.UserApiKey:
        """
        Get API key for the current user

        GET /user/me/api_key

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            API key

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.user.me.get_key()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/user/me/api_key",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.UserApiKey,
            request_options=request_options or default_request_options(),
        )
