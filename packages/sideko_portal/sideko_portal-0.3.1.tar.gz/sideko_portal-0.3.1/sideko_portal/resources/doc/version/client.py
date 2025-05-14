import typing

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
)
from sideko_portal.resources.doc.version.guide import AsyncGuideClient, GuideClient
from sideko_portal.types import models


class VersionClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.guide = GuideClient(base_client=self._base_client)

    def list(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.DocVersion]:
        """
        List versions of a specific Documentation Project

        GET /doc_project/{doc_name}/version

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            A JSON array of versions

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.list(doc_name="my-project")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.DocVersion],
            request_options=request_options or default_request_options(),
        )

    def get(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.DocVersion:
        """
        Get a specific version of an Documentation Project

        GET /doc_project/{doc_name}/version/{doc_version}

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an Documentation project version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.get(
            doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
        )
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.DocVersion,
            request_options=request_options or default_request_options(),
        )


class AsyncVersionClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.guide = AsyncGuideClient(base_client=self._base_client)

    async def list(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.DocVersion]:
        """
        List versions of a specific Documentation Project

        GET /doc_project/{doc_name}/version

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            A JSON array of versions

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.list(doc_name="my-project")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.DocVersion],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.DocVersion:
        """
        Get a specific version of an Documentation Project

        GET /doc_project/{doc_name}/version/{doc_version}

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an Documentation project version

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.get(
            doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
        )
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.DocVersion,
            request_options=request_options or default_request_options(),
        )
