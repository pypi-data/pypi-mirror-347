import typing

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    to_encodable,
)
from sideko_portal.resources.org.theme import AsyncThemeClient, ThemeClient
from sideko_portal.types import models, params


class OrgClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.theme = ThemeClient(base_client=self._base_client)

    def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Organization:
        """
        Get Organization

        Retrieves the organization of the current authenticated user

        GET /organization

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            User organization object

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.org.get()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/organization",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Organization,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        name: str,
        subdomain: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.OrganizationWithRedirect:
        """
        Create a new organization

        POST /organization

        Args:
            name: str
            subdomain: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Organization created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.org.create(name="My Organization", subdomain="my-org")
        ```
        """
        _json = to_encodable(
            item={"name": name, "subdomain": subdomain},
            dump_with=params._SerializerNewOrganization,
        )
        return self._base_client.request(
            method="POST",
            path="/organization",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.OrganizationWithRedirect,
            request_options=request_options or default_request_options(),
        )


class AsyncOrgClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.theme = AsyncThemeClient(base_client=self._base_client)

    async def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Organization:
        """
        Get Organization

        Retrieves the organization of the current authenticated user

        GET /organization

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            User organization object

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.org.get()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/organization",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Organization,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        name: str,
        subdomain: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.OrganizationWithRedirect:
        """
        Create a new organization

        POST /organization

        Args:
            name: str
            subdomain: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Organization created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.org.create(name="My Organization", subdomain="my-org")
        ```
        """
        _json = to_encodable(
            item={"name": name, "subdomain": subdomain},
            dump_with=params._SerializerNewOrganization,
        )
        return await self._base_client.request(
            method="POST",
            path="/organization",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.OrganizationWithRedirect,
            request_options=request_options or default_request_options(),
        )
