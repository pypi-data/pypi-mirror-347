import httpx
import typing
import typing_extensions

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    to_encodable,
)
from sideko_portal.resources.user.me import AsyncMeClient, MeClient
from sideko_portal.types import params


class UserClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.me = MeClient(base_client=self._base_client)

    def invite(
        self,
        *,
        email: str,
        role_definition_id: typing_extensions.Literal[
            "ApiProjectAdmin",
            "ApiProjectContributor",
            "ApiProjectViewer",
            "DocProjectAdmin",
            "DocProjectContributor",
            "DocProjectViewer",
            "OrganizationAdmin",
            "OrganizationManager",
            "OrganizationMember",
        ],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> httpx.Response:
        """
        Invite a user to an organization with a specific role

        POST /user/invite

        Args:
            email: str
            role_definition_id: typing_extensions.Literal["ApiProjectAdmin", "ApiProjectContributor", "ApiProjectViewer", "DocProjectAdmin", "DocProjectContributor", "DocProjectViewer", "OrganizationAdmin", "OrganizationManager", "OrganizationMember"]
            request_options: Additional options to customize the HTTP request

        Returns:
            User invited

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.user.invite(
            email="user@example.com", role_definition_id="ApiProjectAdmin"
        )
        ```
        """
        _json = to_encodable(
            item={"email": email, "role_definition_id": role_definition_id},
            dump_with=params._SerializerInvite,
        )
        return self._base_client.request(
            method="POST",
            path="/user/invite",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=httpx.Response,
            request_options=request_options or default_request_options(),
        )


class AsyncUserClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.me = AsyncMeClient(base_client=self._base_client)

    async def invite(
        self,
        *,
        email: str,
        role_definition_id: typing_extensions.Literal[
            "ApiProjectAdmin",
            "ApiProjectContributor",
            "ApiProjectViewer",
            "DocProjectAdmin",
            "DocProjectContributor",
            "DocProjectViewer",
            "OrganizationAdmin",
            "OrganizationManager",
            "OrganizationMember",
        ],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> httpx.Response:
        """
        Invite a user to an organization with a specific role

        POST /user/invite

        Args:
            email: str
            role_definition_id: typing_extensions.Literal["ApiProjectAdmin", "ApiProjectContributor", "ApiProjectViewer", "DocProjectAdmin", "DocProjectContributor", "DocProjectViewer", "OrganizationAdmin", "OrganizationManager", "OrganizationMember"]
            request_options: Additional options to customize the HTTP request

        Returns:
            User invited

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.user.invite(
            email="user@example.com", role_definition_id="ApiProjectAdmin"
        )
        ```
        """
        _json = to_encodable(
            item={"email": email, "role_definition_id": role_definition_id},
            dump_with=params._SerializerInvite,
        )
        return await self._base_client.request(
            method="POST",
            path="/user/invite",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=httpx.Response,
            request_options=request_options or default_request_options(),
        )
