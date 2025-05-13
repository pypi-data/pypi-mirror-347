import httpx
import typing

from sideko_portal.core import (
    AsyncBaseClient,
    AuthKeyCookie,
    AuthKeyHeader,
    SyncBaseClient,
)
from sideko_portal.environment import Environment, _get_base_url
from sideko_portal.resources.api import ApiClient, AsyncApiClient
from sideko_portal.resources.api_link import ApiLinkClient, AsyncApiLinkClient
from sideko_portal.resources.asset import AssetClient, AsyncAssetClient
from sideko_portal.resources.auth import AsyncAuthClient, AuthClient
from sideko_portal.resources.cli import AsyncCliClient, CliClient
from sideko_portal.resources.doc import AsyncDocClient, DocClient
from sideko_portal.resources.lint import AsyncLintClient, LintClient
from sideko_portal.resources.org import AsyncOrgClient, OrgClient
from sideko_portal.resources.role import AsyncRoleClient, RoleClient
from sideko_portal.resources.sdk import AsyncSdkClient, SdkClient
from sideko_portal.resources.service_account import (
    AsyncServiceAccountClient,
    ServiceAccountClient,
)
from sideko_portal.resources.user import AsyncUserClient, UserClient


class SidekoClient:
    def __init__(
        self,
        *,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None,
        base_url: typing.Optional[str] = None,
        environment: Environment = Environment.PRODUCTION,
        api_key: typing.Optional[str] = None,
        session_cookie: typing.Optional[str] = None,
    ):
        """Initialize root client"""
        self._base_client = SyncBaseClient(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            httpx_client=httpx.Client(timeout=timeout)
            if httpx_client is None
            else httpx_client,
        )
        self._base_client.register_auth(
            "ApiKeyAuth", AuthKeyHeader(header_name="x-sideko-key", val=api_key)
        )
        self._base_client.register_auth(
            "CookieAuth",
            AuthKeyCookie(cookie_name="SIDEKO_SESSION", val=session_cookie),
        )
        self.api = ApiClient(base_client=self._base_client)
        self.api_link = ApiLinkClient(base_client=self._base_client)
        self.doc = DocClient(base_client=self._base_client)
        self.asset = AssetClient(base_client=self._base_client)
        self.role = RoleClient(base_client=self._base_client)
        self.service_account = ServiceAccountClient(base_client=self._base_client)
        self.auth = AuthClient(base_client=self._base_client)
        self.cli = CliClient(base_client=self._base_client)
        self.org = OrgClient(base_client=self._base_client)
        self.sdk = SdkClient(base_client=self._base_client)
        self.user = UserClient(base_client=self._base_client)
        self.lint = LintClient(base_client=self._base_client)


class AsyncSidekoClient:
    def __init__(
        self,
        *,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        base_url: typing.Optional[str] = None,
        environment: Environment = Environment.PRODUCTION,
        api_key: typing.Optional[str] = None,
        session_cookie: typing.Optional[str] = None,
    ):
        """Initialize root client"""
        self._base_client = AsyncBaseClient(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            httpx_client=httpx.AsyncClient(timeout=timeout)
            if httpx_client is None
            else httpx_client,
        )
        self._base_client.register_auth(
            "ApiKeyAuth", AuthKeyHeader(header_name="x-sideko-key", val=api_key)
        )
        self._base_client.register_auth(
            "CookieAuth",
            AuthKeyCookie(cookie_name="SIDEKO_SESSION", val=session_cookie),
        )
        self.api = AsyncApiClient(base_client=self._base_client)
        self.api_link = AsyncApiLinkClient(base_client=self._base_client)
        self.doc = AsyncDocClient(base_client=self._base_client)
        self.asset = AsyncAssetClient(base_client=self._base_client)
        self.role = AsyncRoleClient(base_client=self._base_client)
        self.service_account = AsyncServiceAccountClient(base_client=self._base_client)
        self.auth = AsyncAuthClient(base_client=self._base_client)
        self.cli = AsyncCliClient(base_client=self._base_client)
        self.org = AsyncOrgClient(base_client=self._base_client)
        self.sdk = AsyncSdkClient(base_client=self._base_client)
        self.user = AsyncUserClient(base_client=self._base_client)
        self.lint = AsyncLintClient(base_client=self._base_client)
