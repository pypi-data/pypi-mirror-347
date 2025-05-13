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
from sideko_portal.resources.doc.deployment import (
    AsyncDeploymentClient,
    DeploymentClient,
)
from sideko_portal.resources.doc.preview import AsyncPreviewClient, PreviewClient
from sideko_portal.resources.doc.theme import AsyncThemeClient, ThemeClient
from sideko_portal.resources.doc.version import AsyncVersionClient, VersionClient
from sideko_portal.types import models, params


class DocClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        self.preview = PreviewClient(base_client=self._base_client)
        self.version = VersionClient(base_client=self._base_client)
        self.deployment = DeploymentClient(base_client=self._base_client)
        self.theme = ThemeClient(base_client=self._base_client)

    def delete(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a specific Documentation Project

        DELETE /doc_project/{doc_name}

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Documentation Project deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.delete(doc_name="my-project")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/doc_project/{doc_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.DocProject]:
        """
        List Documentation Projects

        GET /doc_project

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            List of documentation projects you have access to

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.list()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/doc_project",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.DocProject],
            request_options=request_options or default_request_options(),
        )

    def get(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.DocProject:
        """
        Get a specific Documentation Project

        GET /doc_project/{doc_name}

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an Documentation project

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.get(doc_name="my-project")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.DocProject,
            request_options=request_options or default_request_options(),
        )

    def check_preview(
        self,
        *,
        doc_name: str,
        pathname: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> bool:
        """
        A simple check to see if the requesting user has access to the preview doc project

        GET /doc_project/{doc_name}/preview

        Args:
            pathname: relative path within docgen site requesting view permissions
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            User can preview the doc project

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.check_preview(
            doc_name="my-project",
            pathname="%2Freferences%my-api%2Fmy-get-documentation",
        )
        ```
        """
        _query: QueryParams = {}
        if not isinstance(pathname, type_utils.NotGiven):
            encode_query_param(
                _query,
                "pathname",
                to_encodable(item=pathname, dump_with=str),
                style="form",
                explode=True,
            )
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/preview",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=bool,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        doc_name: str,
        logos: typing.Union[
            typing.Optional[params.UpdateDocProjectLogos], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        settings: typing.Union[
            typing.Optional[params.UpdateDocProjectSettings], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.DocProject:
        """
        Update an existing Documentation Project

        PATCH /doc_project/{doc_name}

        Args:
            logos: UpdateDocProjectLogos
            name: str
            settings: UpdateDocProjectSettings
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Documentation Project updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.patch(doc_name="my-project", name="my-company-docs")
        ```
        """
        _json = to_encodable(
            item={"logos": logos, "name": name, "settings": settings},
            dump_with=params._SerializerUpdateDocProject,
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/doc_project/{doc_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.DocProject,
            request_options=request_options or default_request_options(),
        )

    def create(
        self, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.DocProject:
        """
        Create a new Documentation Project

        POST /doc_project

        Args:
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Documentation Project created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.create(name="my-company-docs")
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerNewDocProject
        )
        return self._base_client.request(
            method="POST",
            path="/doc_project",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.DocProject,
            request_options=request_options or default_request_options(),
        )


class AsyncDocClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        self.preview = AsyncPreviewClient(base_client=self._base_client)
        self.version = AsyncVersionClient(base_client=self._base_client)
        self.deployment = AsyncDeploymentClient(base_client=self._base_client)
        self.theme = AsyncThemeClient(base_client=self._base_client)

    async def delete(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a specific Documentation Project

        DELETE /doc_project/{doc_name}

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Documentation Project deleted

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.delete(doc_name="my-project")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/doc_project/{doc_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[models.DocProject]:
        """
        List Documentation Projects

        GET /doc_project

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            List of documentation projects you have access to

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.list()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/doc_project",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.DocProject],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self, *, doc_name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.DocProject:
        """
        Get a specific Documentation Project

        GET /doc_project/{doc_name}

        Args:
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Details of an Documentation project

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.get(doc_name="my-project")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.DocProject,
            request_options=request_options or default_request_options(),
        )

    async def check_preview(
        self,
        *,
        doc_name: str,
        pathname: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> bool:
        """
        A simple check to see if the requesting user has access to the preview doc project

        GET /doc_project/{doc_name}/preview

        Args:
            pathname: relative path within docgen site requesting view permissions
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            User can preview the doc project

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.check_preview(
            doc_name="my-project",
            pathname="%2Freferences%my-api%2Fmy-get-documentation",
        )
        ```
        """
        _query: QueryParams = {}
        if not isinstance(pathname, type_utils.NotGiven):
            encode_query_param(
                _query,
                "pathname",
                to_encodable(item=pathname, dump_with=str),
                style="form",
                explode=True,
            )
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/preview",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=bool,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        doc_name: str,
        logos: typing.Union[
            typing.Optional[params.UpdateDocProjectLogos], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        settings: typing.Union[
            typing.Optional[params.UpdateDocProjectSettings], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.DocProject:
        """
        Update an existing Documentation Project

        PATCH /doc_project/{doc_name}

        Args:
            logos: UpdateDocProjectLogos
            name: str
            settings: UpdateDocProjectSettings
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Documentation Project updated

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.patch(doc_name="my-project", name="my-company-docs")
        ```
        """
        _json = to_encodable(
            item={"logos": logos, "name": name, "settings": settings},
            dump_with=params._SerializerUpdateDocProject,
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/doc_project/{doc_name}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.DocProject,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> models.DocProject:
        """
        Create a new Documentation Project

        POST /doc_project

        Args:
            name: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Documentation Project created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.create(name="my-company-docs")
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerNewDocProject
        )
        return await self._base_client.request(
            method="POST",
            path="/doc_project",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.DocProject,
            request_options=request_options or default_request_options(),
        )
