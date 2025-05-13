import pydantic
import typing_extensions


class Invite(typing_extensions.TypedDict):
    """
    Object for inviting a new user to an organization
    """

    email: typing_extensions.Required[str]

    role_definition_id: typing_extensions.Required[
        typing_extensions.Literal[
            "ApiProjectAdmin",
            "ApiProjectContributor",
            "ApiProjectViewer",
            "DocProjectAdmin",
            "DocProjectContributor",
            "DocProjectViewer",
            "OrganizationAdmin",
            "OrganizationManager",
            "OrganizationMember",
        ]
    ]


class _SerializerInvite(pydantic.BaseModel):
    """
    Serializer for Invite handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    email: str = pydantic.Field(
        alias="email",
    )
    role_definition_id: typing_extensions.Literal[
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
        alias="role_definition_id",
    )
