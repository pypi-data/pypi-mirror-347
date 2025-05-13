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


class ThemeClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Theme:
        """
        Get organization theme

        Retrieves the documentation project theme configured at the organization level

        GET /organization/theme

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Theme attached to organization

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.org.theme.get()
        ```
        """
        return self._base_client.request(
            method="GET",
            path="/organization/theme",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Theme,
            request_options=request_options or default_request_options(),
        )

    def update(
        self,
        *,
        api_reference_group_variant: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_active_button_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_active_button_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_navbar_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_navbar_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_active_button_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_active_button_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_navbar_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_navbar_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Theme:
        """
        Update organization theme

        Update documentation project theme configured at the organization level

        PUT /organization/theme

        Args:
            api_reference_group_variant: set a group variant to collapse all of references under one dropdown in the sidebar
            dark_active_button_bg_color: in HEX format
            dark_active_button_text_color: in HEX format
            dark_bg_color: in HEX format
            dark_navbar_color: in HEX format
            dark_navbar_text_color: in HEX format
            light_active_button_bg_color: in HEX format
            light_active_button_text_color: in HEX format
            light_bg_color: in HEX format
            light_navbar_color: in HEX format
            light_navbar_text_color: in HEX format
            request_options: Additional options to customize the HTTP request

        Returns:
            Updated theme attached to an organization

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.org.theme.update(
            api_reference_group_variant="grouped",
            dark_active_button_bg_color="#FFFFFF",
            dark_active_button_text_color="#FFFFFF",
            dark_bg_color="#FFFFFF",
            dark_navbar_color="#FFFFFF",
            dark_navbar_text_color="#FFFFFF",
            light_active_button_bg_color="#FFFFFF",
            light_active_button_text_color="#FFFFFF",
            light_bg_color="#FFFFFF",
            light_navbar_color="#FFFFFF",
            light_navbar_text_color="#FFFFFF",
        )
        ```
        """
        _json = to_encodable(
            item={
                "api_reference_group_variant": api_reference_group_variant,
                "dark_active_button_bg_color": dark_active_button_bg_color,
                "dark_active_button_text_color": dark_active_button_text_color,
                "dark_bg_color": dark_bg_color,
                "dark_navbar_color": dark_navbar_color,
                "dark_navbar_text_color": dark_navbar_text_color,
                "light_active_button_bg_color": light_active_button_bg_color,
                "light_active_button_text_color": light_active_button_text_color,
                "light_bg_color": light_bg_color,
                "light_navbar_color": light_navbar_color,
                "light_navbar_text_color": light_navbar_text_color,
            },
            dump_with=params._SerializerThemeValues,
        )
        return self._base_client.request(
            method="PUT",
            path="/organization/theme",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Theme,
            request_options=request_options or default_request_options(),
        )


class AsyncThemeClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> models.Theme:
        """
        Get organization theme

        Retrieves the documentation project theme configured at the organization level

        GET /organization/theme

        Args:
            request_options: Additional options to customize the HTTP request

        Returns:
            Theme attached to organization

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.org.theme.get()
        ```
        """
        return await self._base_client.request(
            method="GET",
            path="/organization/theme",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            cast_to=models.Theme,
            request_options=request_options or default_request_options(),
        )

    async def update(
        self,
        *,
        api_reference_group_variant: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_active_button_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_active_button_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_navbar_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        dark_navbar_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_active_button_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_active_button_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_bg_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_navbar_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        light_navbar_text_color: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.Theme:
        """
        Update organization theme

        Update documentation project theme configured at the organization level

        PUT /organization/theme

        Args:
            api_reference_group_variant: set a group variant to collapse all of references under one dropdown in the sidebar
            dark_active_button_bg_color: in HEX format
            dark_active_button_text_color: in HEX format
            dark_bg_color: in HEX format
            dark_navbar_color: in HEX format
            dark_navbar_text_color: in HEX format
            light_active_button_bg_color: in HEX format
            light_active_button_text_color: in HEX format
            light_bg_color: in HEX format
            light_navbar_color: in HEX format
            light_navbar_text_color: in HEX format
            request_options: Additional options to customize the HTTP request

        Returns:
            Updated theme attached to an organization

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.org.theme.update(
            api_reference_group_variant="grouped",
            dark_active_button_bg_color="#FFFFFF",
            dark_active_button_text_color="#FFFFFF",
            dark_bg_color="#FFFFFF",
            dark_navbar_color="#FFFFFF",
            dark_navbar_text_color="#FFFFFF",
            light_active_button_bg_color="#FFFFFF",
            light_active_button_text_color="#FFFFFF",
            light_bg_color="#FFFFFF",
            light_navbar_color="#FFFFFF",
            light_navbar_text_color="#FFFFFF",
        )
        ```
        """
        _json = to_encodable(
            item={
                "api_reference_group_variant": api_reference_group_variant,
                "dark_active_button_bg_color": dark_active_button_bg_color,
                "dark_active_button_text_color": dark_active_button_text_color,
                "dark_bg_color": dark_bg_color,
                "dark_navbar_color": dark_navbar_color,
                "dark_navbar_text_color": dark_navbar_text_color,
                "light_active_button_bg_color": light_active_button_bg_color,
                "light_active_button_text_color": light_active_button_text_color,
                "light_bg_color": light_bg_color,
                "light_navbar_color": light_navbar_color,
                "light_navbar_text_color": light_navbar_text_color,
            },
            dump_with=params._SerializerThemeValues,
        )
        return await self._base_client.request(
            method="PUT",
            path="/organization/theme",
            auth_names=["ApiKeyAuth", "CookieAuth"],
            json=_json,
            cast_to=models.Theme,
            request_options=request_options or default_request_options(),
        )
