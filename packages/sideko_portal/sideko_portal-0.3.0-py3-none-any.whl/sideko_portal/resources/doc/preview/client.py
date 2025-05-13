import typing

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    to_encodable,
)
from sideko_portal.types import models, params


class PreviewClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete_password(
        self,
        *,
        doc_name: str,
        name: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Deletes a preview environment password

        DELETE /doc_project/{doc_name}/password

        Args:
            doc_name: Unique project name or the uuid
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Deleted doc project preview password

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.preview.delete_password(
            doc_name="my-project", name="My customer preview"
        )
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerDocPreviewPasswordName
        )
        self._base_client.request(
            method="DELETE",
            path=f"/doc_project/{doc_name}/password",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list_passwords(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.DocPreviewPassword]:
        """
        Lists generated passwords for a documentation project preview environment

        GET /doc_project/{doc_name}/password

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            The generated passwords for a doc project preview

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.preview.list_passwords(doc_name="my-project")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/password",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.DocPreviewPassword],
            request_options=request_options or default_request_options(),
        )

    def create_password(
        self,
        *,
        doc_name: str,
        name: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.DocPreviewPassword:
        """
        A password generator for a documentation project preview environment

        POST /doc_project/{doc_name}/password

        Args:
            doc_name: Unique project name or the uuid
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            New password generated successfully

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.preview.create_password(
            doc_name="my-project", name="My customer preview"
        )
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerDocPreviewPasswordName
        )
        return self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/password",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.DocPreviewPassword,
            request_options=request_options or default_request_options(),
        )


class AsyncPreviewClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete_password(
        self,
        *,
        doc_name: str,
        name: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Deletes a preview environment password

        DELETE /doc_project/{doc_name}/password

        Args:
            doc_name: Unique project name or the uuid
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Deleted doc project preview password

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.preview.delete_password(
            doc_name="my-project", name="My customer preview"
        )
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerDocPreviewPasswordName
        )
        await self._base_client.request(
            method="DELETE",
            path=f"/doc_project/{doc_name}/password",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list_passwords(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.DocPreviewPassword]:
        """
        Lists generated passwords for a documentation project preview environment

        GET /doc_project/{doc_name}/password

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            The generated passwords for a doc project preview

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.preview.list_passwords(doc_name="my-project")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/password",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.DocPreviewPassword],
            request_options=request_options or default_request_options(),
        )

    async def create_password(
        self,
        *,
        doc_name: str,
        name: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.DocPreviewPassword:
        """
        A password generator for a documentation project preview environment

        POST /doc_project/{doc_name}/password

        Args:
            doc_name: Unique project name or the uuid
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            New password generated successfully

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.preview.create_password(
            doc_name="my-project", name="My customer preview"
        )
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerDocPreviewPasswordName
        )
        return await self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/password",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.DocPreviewPassword,
            request_options=request_options or default_request_options(),
        )
