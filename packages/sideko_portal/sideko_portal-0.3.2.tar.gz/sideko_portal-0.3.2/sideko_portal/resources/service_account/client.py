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


class ServiceAccountClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a service account

        DELETE /service_account/{id}

        Args:
            id: service account id
            request_options: Additional options to customize the HTTP request

        Returns:
            Service account deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.service_account.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/service_account/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.User]:
        """
        List all service accounts in organization

        GET /service_account

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully retrieved service accounts

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.service_account.list()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/service_account",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.User],
            request_options=request_options or default_request_options(),
        )

    def get(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.User:
        """
        Get service account by the ID

        GET /service_account/{id}

        Args:
            id: service account id
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully retrieved service account

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.service_account.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/service_account/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.User,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        name: str,
        object_roles: typing.List[params.ObjectRole],
        expiration: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.UserApiKey:
        """
        Create a new service account with a set of project permissions

        POST /service_account

        Args:
            expiration: UTC datetime when the service account key should expire (ISO 8601 format without timezone), key never expires expiration is not specified
            name: str
            object_roles: typing.List[ObjectRole]
            request_options: Additional options to customize the HTTP request

        Returns:
            Service Account Created, returning API key

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.service_account.create(
            name="Documentation Publisher Service Account",
            object_roles=[
                {
                    "object_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "object_type": "api_project",
                    "role_definition_id": "ApiProjectAdmin",
                }
            ],
            expiration="2025-01-01T00:00:00",
        )
        ```
        """
        _json = to_encodable(
            item={"expiration": expiration, "name": name, "object_roles": object_roles},
            dump_with=params._SerializerNewServiceAccount,
        )
        return self._base_client.request(
            method="POST",
            path="/service_account",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.UserApiKey,
            request_options=request_options or default_request_options(),
        )


class AsyncServiceAccountClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a service account

        DELETE /service_account/{id}

        Args:
            id: service account id
            request_options: Additional options to customize the HTTP request

        Returns:
            Service account deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.service_account.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/service_account/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.User]:
        """
        List all service accounts in organization

        GET /service_account

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully retrieved service accounts

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.service_account.list()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/service_account",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.User],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.User:
        """
        Get service account by the ID

        GET /service_account/{id}

        Args:
            id: service account id
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully retrieved service account

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.service_account.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/service_account/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.User,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        name: str,
        object_roles: typing.List[params.ObjectRole],
        expiration: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.UserApiKey:
        """
        Create a new service account with a set of project permissions

        POST /service_account

        Args:
            expiration: UTC datetime when the service account key should expire (ISO 8601 format without timezone), key never expires expiration is not specified
            name: str
            object_roles: typing.List[ObjectRole]
            request_options: Additional options to customize the HTTP request

        Returns:
            Service Account Created, returning API key

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.service_account.create(
            name="Documentation Publisher Service Account",
            object_roles=[
                {
                    "object_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "object_type": "api_project",
                    "role_definition_id": "ApiProjectAdmin",
                }
            ],
            expiration="2025-01-01T00:00:00",
        )
        ```
        """
        _json = to_encodable(
            item={"expiration": expiration, "name": name, "object_roles": object_roles},
            dump_with=params._SerializerNewServiceAccount,
        )
        return await self._base_client.request(
            method="POST",
            path="/service_account",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.UserApiKey,
            request_options=request_options or default_request_options(),
        )
