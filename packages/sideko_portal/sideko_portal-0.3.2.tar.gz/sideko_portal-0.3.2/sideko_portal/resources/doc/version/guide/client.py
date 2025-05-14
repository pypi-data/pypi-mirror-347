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


class GuideClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def delete(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete a specific guide for a specific version of a documentation project

        DELETE /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Deleted guide

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.delete(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        self._base_client.request(
            method="DELETE",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}",
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
    ) -> typing.List[models.GuideWithChildren]:
        """
        List guides for a specific version of a documentation project

        GET /doc_project/{doc_name}/version/{doc_version}/guide

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Guides listed

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.list(
            doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
        )
        ```
        """
        models.GuideWithChildren.model_rebuild(_types_namespace=models._types_namespace)
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.GuideWithChildren],
            request_options=request_options or default_request_options(),
        )

    def get(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Guide:
        """
        Get a specific guide for a specific version of a documentation project

        GET /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Get guide

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.get(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Guide,
            request_options=request_options or default_request_options(),
        )

    def get_content(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.GuideContent:
        """
        Get content for a specific guide for a specific version of a documentation project

        GET /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}/content

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Get guide mdx content

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.get_content(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}/content",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.GuideContent,
            request_options=request_options or default_request_options(),
        )

    def patch(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        content: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        icon: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        nav_label: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        next_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        prev_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        slug: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        table_of_contents: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Guide:
        """
        Update a specific guide for a specific version of a documentation project

        PATCH /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}

        Args:
            content: str
            icon: lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
            nav_label: the label that shows on the navbar for this guide
            next_id: typing.Optional[str]
            prev_id: typing.Optional[str]
            slug: the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
            table_of_contents: bool
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Updated guide

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.patch(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            icon="house",
        )
        ```
        """
        _json = to_encodable(
            item={
                "content": content,
                "icon": icon,
                "nav_label": nav_label,
                "next_id": next_id,
                "prev_id": prev_id,
                "slug": slug,
                "table_of_contents": table_of_contents,
            },
            dump_with=params._SerializerUpdateGuide,
        )
        return self._base_client.request(
            method="PATCH",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Guide,
            request_options=request_options or default_request_options(),
        )

    def create(
        self,
        *,
        content: str,
        doc_name: str,
        doc_version: typing.Union[str, int],
        is_parent: bool,
        nav_label: str,
        slug: str,
        icon: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        next_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        parent_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        prev_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        table_of_contents: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Guide:
        """
        Create a guide for a specific version of a documentation project

        POST /doc_project/{doc_name}/version/{doc_version}/guide

        Args:
            icon: lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
            next_id: str
            parent_id: str
            prev_id: str
            table_of_contents: bool
            content: str
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            is_parent: bool
            nav_label: the label that shows on the navbar for this guide
            slug: the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
            request_options: Additional options to customize the HTTP request

        Returns:
            Guide created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.create(
            content="string",
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            is_parent=True,
            nav_label="string",
            slug="string",
            icon="house",
        )
        ```
        """
        _json = to_encodable(
            item={
                "icon": icon,
                "next_id": next_id,
                "parent_id": parent_id,
                "prev_id": prev_id,
                "table_of_contents": table_of_contents,
                "content": content,
                "is_parent": is_parent,
                "nav_label": nav_label,
                "slug": slug,
            },
            dump_with=params._SerializerNewGuide,
        )
        return self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Guide,
            request_options=request_options or default_request_options(),
        )

    def reorder(
        self,
        *,
        data: typing.List[params.ReorderGuide],
        doc_name: str,
        doc_version: typing.Union[str, int],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.GuideWithChildren]:
        """
        Reorder guides for a specific version of a documentation project

        POST /doc_project/{doc_name}/version/{doc_version}/guide/reorder

        Args:
            data: typing.List[ReorderGuide]
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Guides reordered

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.doc.version.guide.reorder(
            data=[
                {
                    "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "order": 123,
                    "parent_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                }
            ],
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        models.GuideWithChildren.model_rebuild(_types_namespace=models._types_namespace)
        _json = to_encodable(
            item=data, dump_with=typing.List[params._SerializerReorderGuide]
        )
        return self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/reorder",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=typing.List[models.GuideWithChildren],
            request_options=request_options or default_request_options(),
        )


class AsyncGuideClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def delete(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete a specific guide for a specific version of a documentation project

        DELETE /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Deleted guide

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.delete(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        await self._base_client.request(
            method="DELETE",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}",
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
    ) -> typing.List[models.GuideWithChildren]:
        """
        List guides for a specific version of a documentation project

        GET /doc_project/{doc_name}/version/{doc_version}/guide

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Guides listed

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.list(
            doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
        )
        ```
        """
        models.GuideWithChildren.model_rebuild(_types_namespace=models._types_namespace)
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=typing.List[models.GuideWithChildren],
            request_options=request_options or default_request_options(),
        )

    async def get(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Guide:
        """
        Get a specific guide for a specific version of a documentation project

        GET /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Get guide

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.get(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Guide,
            request_options=request_options or default_request_options(),
        )

    async def get_content(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.GuideContent:
        """
        Get content for a specific guide for a specific version of a documentation project

        GET /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}/content

        Args:
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Get guide mdx content

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.get_content(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}/content",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.GuideContent,
            request_options=request_options or default_request_options(),
        )

    async def patch(
        self,
        *,
        doc_name: str,
        doc_version: typing.Union[str, int],
        guide_id: str,
        content: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        icon: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        nav_label: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        next_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        prev_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        slug: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        table_of_contents: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Guide:
        """
        Update a specific guide for a specific version of a documentation project

        PATCH /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}

        Args:
            content: str
            icon: lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
            nav_label: the label that shows on the navbar for this guide
            next_id: typing.Optional[str]
            prev_id: typing.Optional[str]
            slug: the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
            table_of_contents: bool
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            guide_id: str
            request_options: Additional options to customize the HTTP request

        Returns:
            Updated guide

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.patch(
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            icon="house",
        )
        ```
        """
        _json = to_encodable(
            item={
                "content": content,
                "icon": icon,
                "nav_label": nav_label,
                "next_id": next_id,
                "prev_id": prev_id,
                "slug": slug,
                "table_of_contents": table_of_contents,
            },
            dump_with=params._SerializerUpdateGuide,
        )
        return await self._base_client.request(
            method="PATCH",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Guide,
            request_options=request_options or default_request_options(),
        )

    async def create(
        self,
        *,
        content: str,
        doc_name: str,
        doc_version: typing.Union[str, int],
        is_parent: bool,
        nav_label: str,
        slug: str,
        icon: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        next_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        parent_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        prev_id: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        table_of_contents: typing.Union[
            typing.Optional[bool], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Guide:
        """
        Create a guide for a specific version of a documentation project

        POST /doc_project/{doc_name}/version/{doc_version}/guide

        Args:
            icon: lucide icon name for guide, see https://lucide.dev/icons/ for complete list of options
            next_id: str
            parent_id: str
            prev_id: str
            table_of_contents: bool
            content: str
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            is_parent: bool
            nav_label: the label that shows on the navbar for this guide
            slug: the url slug (route) for this guide. Must be one word. Use - for spaces. optimize the name for SEO
            request_options: Additional options to customize the HTTP request

        Returns:
            Guide created

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.create(
            content="string",
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            is_parent=True,
            nav_label="string",
            slug="string",
            icon="house",
        )
        ```
        """
        _json = to_encodable(
            item={
                "icon": icon,
                "next_id": next_id,
                "parent_id": parent_id,
                "prev_id": prev_id,
                "table_of_contents": table_of_contents,
                "content": content,
                "is_parent": is_parent,
                "nav_label": nav_label,
                "slug": slug,
            },
            dump_with=params._SerializerNewGuide,
        )
        return await self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Guide,
            request_options=request_options or default_request_options(),
        )

    async def reorder(
        self,
        *,
        data: typing.List[params.ReorderGuide],
        doc_name: str,
        doc_version: typing.Union[str, int],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.GuideWithChildren]:
        """
        Reorder guides for a specific version of a documentation project

        POST /doc_project/{doc_name}/version/{doc_version}/guide/reorder

        Args:
            data: typing.List[ReorderGuide]
            doc_name: Unique project name or the uuid
            doc_version: typing.Union[str, int]
            request_options: Additional options to customize the HTTP request

        Returns:
            Guides reordered

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.doc.version.guide.reorder(
            data=[
                {
                    "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                    "order": 123,
                    "parent_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
                }
            ],
            doc_name="my-project",
            doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        )
        ```
        """
        models.GuideWithChildren.model_rebuild(_types_namespace=models._types_namespace)
        _json = to_encodable(
            item=data, dump_with=typing.List[params._SerializerReorderGuide]
        )
        return await self._base_client.request(
            method="POST",
            path=f"/doc_project/{doc_name}/version/{doc_version}/guide/reorder",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=typing.List[models.GuideWithChildren],
            request_options=request_options or default_request_options(),
        )
