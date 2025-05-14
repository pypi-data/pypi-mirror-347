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


class DeploymentClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def list(
        self,
        *,
        doc_name: str,
        limit: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        target: typing.Union[
            typing.Optional[typing_extensions.Literal["Preview", "Production"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.Deployment]:
        """
        List deployments for a specific documentation project

        Retrieves all deployments for a doc project

        GET /doc_project/{doc_name}/deployment

        Args:
            limit: int
            target: typing_extensions.Literal["Preview", "Production"]
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Deployments matching the query

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.deployment.list(doc_name="my-project")
        ```
        """
        _query: QueryParams = {}
        if not isinstance(limit, type_utils.NotGiven):
            encode_query_param(
                _query,
                "limit",
                to_encodable(item=limit, dump_with=int),
                style="form",
                explode=True,
            )
        if not isinstance(target, type_utils.NotGiven):
            encode_query_param(
                _query,
                "target",
                to_encodable(
                    item=target,
                    dump_with=typing_extensions.Literal["Preview", "Production"],
                ),
                style="form",
                explode=True,
            )
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/deployment",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.Deployment],
            request_options=request_options or default_request_options(),
        )

    def get(
        self,
        *,
        deployment_id: str,
        doc_name: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Deployment:
        """
        Get a specific deployment for a specific documentation project

        Retrieves single deployment

        GET /doc_project/{doc_name}/deployment/{deployment_id}

        Args:
            deployment_id: str
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieved deployment

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.deployment.get(
            deployment_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", doc_name="my-project"
        )
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/deployment/{deployment_id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Deployment,
            request_options=request_options or default_request_options(),
        )

    def trigger(
        self,
        *,
        doc_name: str,
        target: typing_extensions.Literal["Preview", "Production"],
        doc_version_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Deployment:
        """
        Deploy a new generated version of documentation with linked guides & APIs

        Deploys a new generated version of documentation with linked guides & APIs

        POST /doc_project/{doc_name}/deployment

        Args:
            doc_version_id: str
            doc_name: Unique project name or the uuid
            target: typing_extensions.Literal["Preview", "Production"]
            request_options: Additional options to customize the HTTP request

        Returns:
            New deployment triggered

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.deployment.trigger(doc_name="my-project", target="Preview")
        ```
        """
        _json = to_encodable(
            item={"doc_version_id": doc_version_id, "target": target},
            dump_with=params._SerializerNewDeployment,
        )
        return self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/deployment",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Deployment,
            request_options=request_options or default_request_options(),
        )


class AsyncDeploymentClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def list(
        self,
        *,
        doc_name: str,
        limit: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        target: typing.Union[
            typing.Optional[typing_extensions.Literal["Preview", "Production"]],
            type_utils.NotGiven,
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.Deployment]:
        """
        List deployments for a specific documentation project

        Retrieves all deployments for a doc project

        GET /doc_project/{doc_name}/deployment

        Args:
            limit: int
            target: typing_extensions.Literal["Preview", "Production"]
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Deployments matching the query

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.deployment.list(doc_name="my-project")
        ```
        """
        _query: QueryParams = {}
        if not isinstance(limit, type_utils.NotGiven):
            encode_query_param(
                _query,
                "limit",
                to_encodable(item=limit, dump_with=int),
                style="form",
                explode=True,
            )
        if not isinstance(target, type_utils.NotGiven):
            encode_query_param(
                _query,
                "target",
                to_encodable(
                    item=target,
                    dump_with=typing_extensions.Literal["Preview", "Production"],
                ),
                style="form",
                explode=True,
            )
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/deployment",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=typing.List[models.Deployment],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self,
        *,
        deployment_id: str,
        doc_name: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Deployment:
        """
        Get a specific deployment for a specific documentation project

        Retrieves single deployment

        GET /doc_project/{doc_name}/deployment/{deployment_id}

        Args:
            deployment_id: str
            doc_name: Unique project name or the uuid
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieved deployment

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.deployment.get(
            deployment_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", doc_name="my-project"
        )
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/deployment/{deployment_id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Deployment,
            request_options=request_options or default_request_options(),
        )

    async def trigger(
        self,
        *,
        doc_name: str,
        target: typing_extensions.Literal["Preview", "Production"],
        doc_version_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Deployment:
        """
        Deploy a new generated version of documentation with linked guides & APIs

        Deploys a new generated version of documentation with linked guides & APIs

        POST /doc_project/{doc_name}/deployment

        Args:
            doc_version_id: str
            doc_name: Unique project name or the uuid
            target: typing_extensions.Literal["Preview", "Production"]
            request_options: Additional options to customize the HTTP request

        Returns:
            New deployment triggered

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.deployment.trigger(doc_name="my-project", target="Preview")
        ```
        """
        _json = to_encodable(
            item={"doc_version_id": doc_version_id, "target": target},
            dump_with=params._SerializerNewDeployment,
        )
        return await self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/deployment",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Deployment,
            request_options=request_options or default_request_options(),
        )
