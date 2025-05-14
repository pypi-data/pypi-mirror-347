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
from sideko_portal.resources.api_link.group import AsyncGroupClient, GroupClient
from sideko_portal.types import models, params


class ApiLinkClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.group = GroupClient(base_client=self._base_client)

    def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Removes an API link

        DELETE /api_link/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/api_link/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.ApiLink]:
        """
        List API links for doc version

        GET /api_link

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieve API links for a doc version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.list(
            doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
        )
        ```
        """
        _query: QueryParams = {}
        encode_query_param(
            _query,
            "doc_name",
            to_encodable(item=doc_name, dump_with=str),
            style="form",
            explode=True,
        )
        encode_query_param(
            _query,
            "doc_version",
            to_encodable(item=doc_version, dump_with=typing.Union[str, int]),
            style="form",
            explode=True,
        )
        return self._base_client.request(
            method="GET",
            path="/api_link",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.ApiLink],
            request_options=request_options or default_request_options(),
        )

    def get(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.ApiLink:
        """
        Retrieve single API link

        GET /api_link/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieved api link

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/api_link/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.ApiLink,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        id: str,
        api_version: typing.Union[
            typing.Optional[params.UpdateApiLinkApiVersion], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        build_request_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        include_mock_server: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        nav_label: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        policy: typing.Union[
            typing.Optional[typing_extensions.Literal["latest", "pinned"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        slug: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLink:
        """
        Updates an API link

        PATCH /api_link/{id}

        Args:
            api_version: the api version can only be patched on api links with a `pinned` policy
            build_request_enabled: bool
            include_mock_server: automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
            nav_label: str
            policy: defines how the link should be automatically updated as new API version are added
            slug: str
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        _json = to_encodable(
            item={
                "api_version": api_version,
                "build_request_enabled": build_request_enabled,
                "include_mock_server": include_mock_server,
                "nav_label": nav_label,
                "policy": policy,
                "slug": slug,
            },
            dump_with=params._SerializerUpdateApiLink,
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/api_link/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLink,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        doc_version_id: str,
        group_id: str,
        nav_label: str,
        policy: typing.Union[params.LatestApiLinkPolicy, params.PinnedApiLinkPolicy],
        slug: str,
        build_request_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        include_mock_server: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLink:
        """
        Links API Version to Documentation project version with a specified update policy

        POST /api_link

        Args:
            build_request_enabled: bool
            include_mock_server: automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
            doc_version_id: str
            group_id: str
            nav_label: str
            policy: typing.Union[LatestApiLinkPolicy, PinnedApiLinkPolicy]
            slug: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.create(
            doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            group_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            nav_label="string",
            policy={"api_id": "my-api", "type_": "latest"},
            slug="string",
        )
        ```
        """
        _json = to_encodable(
            item={
                "build_request_enabled": build_request_enabled,
                "include_mock_server": include_mock_server,
                "doc_version_id": doc_version_id,
                "group_id": group_id,
                "nav_label": nav_label,
                "policy": policy,
                "slug": slug,
            },
            dump_with=params._SerializerNewApiLink,
        )
        return self._base_client.request(
            method="POST",
            path="/api_link",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLink,
            request_options=request_options or default_request_options(),
        )

    def reorder(
        self,
        *,
        doc_version_id: str,
        groups: typing.List[params.ApiLinkGroupReorder],
        links: typing.List[params.ApiLinkReorder],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiReorder:
        """
        Reorder API links and groups

        POST /api_link/reorder

        Args:
            doc_version_id: str
            groups: typing.List[ApiLinkGroupReorder]
            links: typing.List[ApiLinkReorder]
            request_options: Additional options to customize the HTTP request

        Returns:
            successfully reordered

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.reorder(
            doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            groups=[{"id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", "order": 123}],
            links=[
                {
                    "group_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "order": 123,
                }
            ],
        )
        ```
        """
        _json = to_encodable(
            item={"doc_version_id": doc_version_id, "groups": groups, "links": links},
            dump_with=params._SerializerApiReorder,
        )
        return self._base_client.request(
            method="POST",
            path="/api_link/reorder",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiReorder,
            request_options=request_options or default_request_options(),
        )


class AsyncApiLinkClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.group = AsyncGroupClient(base_client=self._base_client)

    async def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Removes an API link

        DELETE /api_link/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/api_link/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.ApiLink]:
        """
        List API links for doc version

        GET /api_link

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieve API links for a doc version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.list(
            doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
        )
        ```
        """
        _query: QueryParams = {}
        encode_query_param(
            _query,
            "doc_name",
            to_encodable(item=doc_name, dump_with=str),
            style="form",
            explode=True,
        )
        encode_query_param(
            _query,
            "doc_version",
            to_encodable(item=doc_version, dump_with=typing.Union[str, int]),
            style="form",
            explode=True,
        )
        return await self._base_client.request(
            method="GET",
            path="/api_link",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.ApiLink],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.ApiLink:
        """
        Retrieve single API link

        GET /api_link/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieved api link

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/api_link/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.ApiLink,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        id: str,
        api_version: typing.Union[
            typing.Optional[params.UpdateApiLinkApiVersion], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        build_request_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        include_mock_server: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        nav_label: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        policy: typing.Union[
            typing.Optional[typing_extensions.Literal["latest", "pinned"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        slug: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLink:
        """
        Updates an API link

        PATCH /api_link/{id}

        Args:
            api_version: the api version can only be patched on api links with a `pinned` policy
            build_request_enabled: bool
            include_mock_server: automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
            nav_label: str
            policy: defines how the link should be automatically updated as new API version are added
            slug: str
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        _json = to_encodable(
            item={
                "api_version": api_version,
                "build_request_enabled": build_request_enabled,
                "include_mock_server": include_mock_server,
                "nav_label": nav_label,
                "policy": policy,
                "slug": slug,
            },
            dump_with=params._SerializerUpdateApiLink,
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/api_link/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLink,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        doc_version_id: str,
        group_id: str,
        nav_label: str,
        policy: typing.Union[params.LatestApiLinkPolicy, params.PinnedApiLinkPolicy],
        slug: str,
        build_request_enabled: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        include_mock_server: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLink:
        """
        Links API Version to Documentation project version with a specified update policy

        POST /api_link

        Args:
            build_request_enabled: bool
            include_mock_server: automatically add the sideko mock server as one of the server options when building a request in the api reference (requires mock server to be enabled on the linked Api Version)
            doc_version_id: str
            group_id: str
            nav_label: str
            policy: typing.Union[LatestApiLinkPolicy, PinnedApiLinkPolicy]
            slug: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.create(
            doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            group_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            nav_label="string",
            policy={"api_id": "my-api", "type_": "latest"},
            slug="string",
        )
        ```
        """
        _json = to_encodable(
            item={
                "build_request_enabled": build_request_enabled,
                "include_mock_server": include_mock_server,
                "doc_version_id": doc_version_id,
                "group_id": group_id,
                "nav_label": nav_label,
                "policy": policy,
                "slug": slug,
            },
            dump_with=params._SerializerNewApiLink,
        )
        return await self._base_client.request(
            method="POST",
            path="/api_link",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLink,
            request_options=request_options or default_request_options(),
        )

    async def reorder(
        self,
        *,
        doc_version_id: str,
        groups: typing.List[params.ApiLinkGroupReorder],
        links: typing.List[params.ApiLinkReorder],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiReorder:
        """
        Reorder API links and groups

        POST /api_link/reorder

        Args:
            doc_version_id: str
            groups: typing.List[ApiLinkGroupReorder]
            links: typing.List[ApiLinkReorder]
            request_options: Additional options to customize the HTTP request

        Returns:
            successfully reordered

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.reorder(
            doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            groups=[{"id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", "order": 123}],
            links=[
                {
                    "group_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "order": 123,
                }
            ],
        )
        ```
        """
        _json = to_encodable(
            item={"doc_version_id": doc_version_id, "groups": groups, "links": links},
            dump_with=params._SerializerApiReorder,
        )
        return await self._base_client.request(
            method="POST",
            path="/api_link/reorder",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiReorder,
            request_options=request_options or default_request_options(),
        )
