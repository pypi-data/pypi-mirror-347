import pydantic


class OrganizationFeatures(pydantic.BaseModel):
    """
    OrganizationFeatures
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    allow_sdk_cli: bool = pydantic.Field(
        alias="allow_sdk_cli",
    )
    """
    Is the organization allowed to generated SDKs for target cli
    """
    allow_sdk_go: bool = pydantic.Field(
        alias="allow_sdk_go",
    )
    """
    Is the organization allowed to generated SDKs for target go
    """
    allow_sdk_java: bool = pydantic.Field(
        alias="allow_sdk_java",
    )
    """
    Is the organization allowed to generated SDKs for target java
    """
    allow_sdk_python: bool = pydantic.Field(
        alias="allow_sdk_python",
    )
    """
    Is the organization allowed to generated SDKs for target python
    """
    allow_sdk_rust: bool = pydantic.Field(
        alias="allow_sdk_rust",
    )
    """
    Is the organization allowed to generated SDKs for target rust
    """
    allow_sdk_tests: bool = pydantic.Field(
        alias="allow_sdk_tests",
    )
    """
    Is the organization allowed to generated tests with it's SDKs
    """
    allow_sdk_typescript: bool = pydantic.Field(
        alias="allow_sdk_typescript",
    )
    """
    Is the organization allowed to generated SDKs for target typescript
    """
    max_api_projects: int = pydantic.Field(
        alias="max_api_projects",
    )
    """
    Maximum number of APIs allowed for the organization
    """
    max_doc_projects: int = pydantic.Field(
        alias="max_doc_projects",
    )
    """
    Maximum number of documentation projects allowed for the organization
    """
    max_mock_servers: int = pydantic.Field(
        alias="max_mock_servers",
    )
    """
    Maximum number of mock servers allowed for this organization
    """
    max_sdk_api_methods: int = pydantic.Field(
        alias="max_sdk_api_methods",
    )
    """
    Maximum number of SDK methods allowed in a generation
    """
    max_service_accounts: int = pydantic.Field(
        alias="max_service_accounts",
    )
    """
    Maximum number of service accounts allowed for this organization
    """
    max_teammates: int = pydantic.Field(
        alias="max_teammates",
    )
    """
    Maximum number of team members allowed for this organization
    """
