import typing

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


class GroupClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Deletes the api group and all its links

        DELETE /api_link_group/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API link group deleted with all links in the group

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.group.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/api_link_group/{id}",
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
    ) -> typing.List[models.ApiLinkGroup]:
        """
        List API groups for doc version

        GET /api_link_group

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            api groups

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.group.list(
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
            path="/api_link_group",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.ApiLinkGroup],
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        id: str,
        nav_label: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        slug: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLinkGroup:
        """
        Updates API link group

        PATCH /api_link_group/{id}

        Args:
            nav_label: str
            slug: str
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API link group updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.group.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        _json = to_encodable(
            item={"nav_label": nav_label, "slug": slug},
            dump_with=params._SerializerUpdateApiLinkGroup,
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/api_link_group/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLinkGroup,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        doc_version_id: str,
        nav_label: str,
        slug: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLinkGroup:
        """
        Create API group to organize API links

        POST /api_link_group

        Args:
            doc_version_id: str
            nav_label: str
            slug: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link group created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.api_link.group.create(
            doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            nav_label="string",
            slug="string",
        )
        ```
        """
        _json = to_encodable(
            item={
                "doc_version_id": doc_version_id,
                "nav_label": nav_label,
                "slug": slug,
            },
            dump_with=params._SerializerNewApiLinkGroup,
        )
        return self._base_client.request(
            method="POST",
            path="/api_link_group",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLinkGroup,
            request_options=request_options or default_request_options(),
        )


class AsyncGroupClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Deletes the api group and all its links

        DELETE /api_link_group/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API link group deleted with all links in the group

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.group.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/api_link_group/{id}",
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
    ) -> typing.List[models.ApiLinkGroup]:
        """
        List API groups for doc version

        GET /api_link_group

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            api groups

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.group.list(
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
            path="/api_link_group",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.ApiLinkGroup],
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        id: str,
        nav_label: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        slug: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLinkGroup:
        """
        Updates API link group

        PATCH /api_link_group/{id}

        Args:
            nav_label: str
            slug: str
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            API link group updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.group.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        _json = to_encodable(
            item={"nav_label": nav_label, "slug": slug},
            dump_with=params._SerializerUpdateApiLinkGroup,
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/api_link_group/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLinkGroup,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        doc_version_id: str,
        nav_label: str,
        slug: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ApiLinkGroup:
        """
        Create API group to organize API links

        POST /api_link_group

        Args:
            doc_version_id: str
            nav_label: str
            slug: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Link group created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.api_link.group.create(
            doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            nav_label="string",
            slug="string",
        )
        ```
        """
        _json = to_encodable(
            item={
                "doc_version_id": doc_version_id,
                "nav_label": nav_label,
                "slug": slug,
            },
            dump_with=params._SerializerNewApiLinkGroup,
        )
        return await self._base_client.request(
            method="POST",
            path="/api_link_group",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.ApiLinkGroup,
            request_options=request_options or default_request_options(),
        )
