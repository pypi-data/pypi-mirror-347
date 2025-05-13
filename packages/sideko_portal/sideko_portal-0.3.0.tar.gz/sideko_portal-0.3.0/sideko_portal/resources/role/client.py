import typing
import typing_extensions

from sideko_portal.core import (
    AsyncBaseClient,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_query_param,
    to_encodable,
    type_utils,
)
from sideko_portal.types import models, params


class RoleClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete role and all associated permissions

        DELETE /role/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Role deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.role.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/role/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self,
        *,
        object_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        object_type: typing.Union[
            typing.Optional[
                typing_extensions.Literal["api_project", "doc_project", "organization"]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        user_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.Role]:
        """
        List roles

        GET /role

        Args:
            object_id: filter roles by object id
            object_type: The object types that roles can be assigned to.
            user_id: filter roles by user id
            request_options: Additional options to customize the HTTP request

        Returns:
            Roles attached to queried object

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.role.list()
        ```
        """
        _query: QueryParams = {}
        if not isinstance(object_id, type_utils.NotGiven):
            encode_query_param(
                _query,
                "object_id",
                to_encodable(item=object_id, dump_with=str),
                style="form",
                explode=True,
            )
        if not isinstance(object_type, type_utils.NotGiven):
            encode_query_param(
                _query,
                "object_type",
                to_encodable(
                    item=object_type,
                    dump_with=typing_extensions.Literal[
                        "api_project", "doc_project", "organization"
                    ],
                ),
                style="form",
                explode=True,
            )
        if not isinstance(user_id, type_utils.NotGiven):
            encode_query_param(
                _query,
                "user_id",
                to_encodable(item=user_id, dump_with=str),
                style="form",
                explode=True,
            )
        return self._base_client.request(
            method="GET",
            path="/role",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.Role],
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        object_id: str,
        object_type: typing_extensions.Literal[
            "api_project", "doc_project", "organization"
        ],
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
        user_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Role:
        """
        Create a new role

        POST /role

        Args:
            object_id: The unique identifier of the Sideko object
            object_type: The object types that roles can be assigned to.
            role_definition_id: typing_extensions.Literal["ApiProjectAdmin", "ApiProjectContributor", "ApiProjectViewer", "DocProjectAdmin", "DocProjectContributor", "DocProjectViewer", "OrganizationAdmin", "OrganizationManager", "OrganizationMember"]
            user_id: unique identifier for the user that the role will be granted to
            request_options: Additional options to customize the HTTP request

        Returns:
            Role created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.role.create(
            object_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            object_type="api_project",
            role_definition_id="ApiProjectAdmin",
            user_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        _json = to_encodable(
            item={
                "object_id": object_id,
                "object_type": object_type,
                "role_definition_id": role_definition_id,
                "user_id": user_id,
            },
            dump_with=params._SerializerNewRole,
        )
        return self._base_client.request(
            method="POST",
            path="/role",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Role,
            request_options=request_options or default_request_options(),
        )


class AsyncRoleClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete role and all associated permissions

        DELETE /role/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Role deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.role.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/role/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self,
        *,
        object_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        object_type: typing.Union[
            typing.Optional[
                typing_extensions.Literal["api_project", "doc_project", "organization"]
            ],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        user_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.Role]:
        """
        List roles

        GET /role

        Args:
            object_id: filter roles by object id
            object_type: The object types that roles can be assigned to.
            user_id: filter roles by user id
            request_options: Additional options to customize the HTTP request

        Returns:
            Roles attached to queried object

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.role.list()
        ```
        """
        _query: QueryParams = {}
        if not isinstance(object_id, type_utils.NotGiven):
            encode_query_param(
                _query,
                "object_id",
                to_encodable(item=object_id, dump_with=str),
                style="form",
                explode=True,
            )
        if not isinstance(object_type, type_utils.NotGiven):
            encode_query_param(
                _query,
                "object_type",
                to_encodable(
                    item=object_type,
                    dump_with=typing_extensions.Literal[
                        "api_project", "doc_project", "organization"
                    ],
                ),
                style="form",
                explode=True,
            )
        if not isinstance(user_id, type_utils.NotGiven):
            encode_query_param(
                _query,
                "user_id",
                to_encodable(item=user_id, dump_with=str),
                style="form",
                explode=True,
            )
        return await self._base_client.request(
            method="GET",
            path="/role",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.Role],
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        object_id: str,
        object_type: typing_extensions.Literal[
            "api_project", "doc_project", "organization"
        ],
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
        user_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Role:
        """
        Create a new role

        POST /role

        Args:
            object_id: The unique identifier of the Sideko object
            object_type: The object types that roles can be assigned to.
            role_definition_id: typing_extensions.Literal["ApiProjectAdmin", "ApiProjectContributor", "ApiProjectViewer", "DocProjectAdmin", "DocProjectContributor", "DocProjectViewer", "OrganizationAdmin", "OrganizationManager", "OrganizationMember"]
            user_id: unique identifier for the user that the role will be granted to
            request_options: Additional options to customize the HTTP request

        Returns:
            Role created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.role.create(
            object_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            object_type="api_project",
            role_definition_id="ApiProjectAdmin",
            user_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        _json = to_encodable(
            item={
                "object_id": object_id,
                "object_type": object_type,
                "role_definition_id": role_definition_id,
                "user_id": user_id,
            },
            dump_with=params._SerializerNewRole,
        )
        return await self._base_client.request(
            method="POST",
            path="/role",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Role,
            request_options=request_options or default_request_options(),
        )
