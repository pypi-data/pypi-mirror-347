import typing

from sideko_portal.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
)
from sideko_portal.types import models


class CliClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def check_updates(
        self,
        *,
        cli_version: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.CliUpdate]:
        """
        Checks if current CLI has updates

        GET /cli/updates/{cli_version}

        Args:
            cli_version: semver of running cli
            request_options: Additional options to customize the HTTP request

        Returns:
            List of updates at different levels available for cli

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.cli.check_updates(cli_version="0.1.0")
        ```
        """
        return self._base_client.request(
            method="GET",
            path=f"/cli/updates/{cli_version}",
            cast_to=typing.List[models.CliUpdate],
            request_options=request_options or default_request_options(),
        )


class AsyncCliClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def check_updates(
        self,
        *,
        cli_version: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[models.CliUpdate]:
        """
        Checks if current CLI has updates

        GET /cli/updates/{cli_version}

        Args:
            cli_version: semver of running cli
            request_options: Additional options to customize the HTTP request

        Returns:
            List of updates at different levels available for cli

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.cli.check_updates(cli_version="0.1.0")
        ```
        """
        return await self._base_client.request(
            method="GET",
            path=f"/cli/updates/{cli_version}",
            cast_to=typing.List[models.CliUpdate],
            request_options=request_options or default_request_options(),
        )
