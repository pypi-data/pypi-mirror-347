import httpx
import typing

from sideko_portal.core import (
    AsyncBaseClient,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_query_param,
    filter_not_given,
    to_encodable,
    type_utils,
)
from sideko_portal.types import models, params


class AssetClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete Asset

        Delete a media asset in your organization

        DELETE /organization/asset/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully deleted the asset and it's contents

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.asset.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/organization/asset/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    def list(
        self,
        *,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        page: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ListAssetsPage:
        """
        List Assets

        Get all media assets for an organization

        GET /organization/asset

        Args:
            name: str
            page: int
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieved organization assets

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.asset.list()
        ```
        """
        _query: QueryParams = {}
        if not isinstance(name, type_utils.NotGiven):
            encode_query_param(
                _query,
                "name",
                to_encodable(item=name, dump_with=str),
                style="form",
                explode=True,
            )
        if not isinstance(page, type_utils.NotGiven):
            encode_query_param(
                _query,
                "page",
                to_encodable(item=page, dump_with=int),
                style="form",
                explode=True,
            )
        return self._base_client.request(
            method="GET",
            path="/organization/asset",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=models.ListAssetsPage,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        id: str,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Asset:
        """
        Update Asset

        Update a media asset in your organization

        PATCH /organization/asset/{id}

        Args:
            name: Asset name (without any extension)
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully deleted the asset and it's contents

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.asset.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerUpdateAsset
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/organization/asset/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Asset,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        file: httpx._types.FileTypes,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.Asset]:
        """
        Upload Assets

        Add a media asset like logos or other media to an organization

        POST /organization/asset

        Args:
            file: httpx._types.FileTypes
            request_options: Additional options to customize the HTTP request

        Returns:
            Added assets to organization

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.asset.create(file=open("uploads/image.png", "rb"))
        ```
        """
        _data = to_encodable(item={"file": file}, dump_with=params._SerializerFile)
        _files = params._SerializerFile.get_files_from_typed_dict(
            filter_not_given({"file": file})
        )
        return self._base_client.request(
            method="POST",
            path="/organization/asset",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=typing.List[models.Asset],
            request_options=request_options or default_request_options(),
        )


class AsyncAssetClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete(
        self, *, id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete Asset

        Delete a media asset in your organization

        DELETE /organization/asset/{id}

        Args:
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully deleted the asset and it's contents

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.asset.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/organization/asset/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=type(None),
            request_options=request_options or default_request_options(),
        )

    async def list(
        self,
        *,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        page: typing.Union[
            typing.Optional[int], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ListAssetsPage:
        """
        List Assets

        Get all media assets for an organization

        GET /organization/asset

        Args:
            name: str
            page: int
            request_options: Additional options to customize the HTTP request

        Returns:
            Retrieved organization assets

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.asset.list()
        ```
        """
        _query: QueryParams = {}
        if not isinstance(name, type_utils.NotGiven):
            encode_query_param(
                _query,
                "name",
                to_encodable(item=name, dump_with=str),
                style="form",
                explode=True,
            )
        if not isinstance(page, type_utils.NotGiven):
            encode_query_param(
                _query,
                "page",
                to_encodable(item=page, dump_with=int),
                style="form",
                explode=True,
            )
        return await self._base_client.request(
            method="GET",
            path="/organization/asset",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            query_params=_query,
            cast_to=models.ListAssetsPage,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        id: str,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Asset:
        """
        Update Asset

        Update a media asset in your organization

        PATCH /organization/asset/{id}

        Args:
            name: Asset name (without any extension)
            id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Successfully deleted the asset and it's contents

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.asset.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
        ```
        """
        _json = to_encodable(
            item={"name": name}, dump_with=params._SerializerUpdateAsset
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/organization/asset/{id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Asset,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        file: httpx._types.FileTypes,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.Asset]:
        """
        Upload Assets

        Add a media asset like logos or other media to an organization

        POST /organization/asset

        Args:
            file: httpx._types.FileTypes
            request_options: Additional options to customize the HTTP request

        Returns:
            Added assets to organization

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.asset.create(file=open("uploads/image.png", "rb"))
        ```
        """
        _data = to_encodable(item={"file": file}, dump_with=params._SerializerFile)
        _files = params._SerializerFile.get_files_from_typed_dict(
            filter_not_given({"file": file})
        )
        return await self._base_client.request(
            method="POST",
            path="/organization/asset",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            data=_data,
            files=_files,
            cast_to=typing.List[models.Asset],
            request_options=request_options or default_request_options(),
        )
