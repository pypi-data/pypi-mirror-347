import pydantic
import typing
import typing_extensions


class RoleDefinition(pydantic.BaseModel):
    """
    RoleDefinition
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    actions: typing.List[
        typing_extensions.Literal[
            "api_project_delete",
            "api_project_read",
            "api_project_update",
            "api_project_version_create",
            "api_project_version_delete",
            "api_project_version_read",
            "api_project_version_update",
            "audit_log_read",
            "doc_project_delete",
            "doc_project_publish_preview",
            "doc_project_publish_production",
            "doc_project_read",
            "doc_project_update",
            "doc_project_version_read",
            "doc_project_version_update",
            "organization_create_api_project",
            "organization_create_doc_project",
            "organization_read_theme",
            "organization_update_theme",
            "role_create",
            "role_delete",
            "role_read",
        ]
    ] = pydantic.Field(
        alias="actions",
    )
    display_name: str = pydantic.Field(
        alias="display_name",
    )
    id: typing_extensions.Literal[
        "ApiProjectAdmin",
        "ApiProjectContributor",
        "ApiProjectViewer",
        "DocProjectAdmin",
        "DocProjectContributor",
        "DocProjectViewer",
        "OrganizationAdmin",
        "OrganizationManager",
        "OrganizationMember",
    ] = pydantic.Field(
        alias="id",
    )
