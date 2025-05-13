import pydantic
import typing_extensions


class NewRole(typing_extensions.TypedDict):
    """
    NewRole
    """

    object_id: typing_extensions.Required[str]
    """
    The unique identifier of the Sideko object
    """

    object_type: typing_extensions.Required[
        typing_extensions.Literal["api_project", "doc_project", "organization"]
    ]
    """
    The object types that roles can be assigned to.
    """

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

    user_id: typing_extensions.Required[str]
    """
    unique identifier for the user that the role will be granted to
    """


class _SerializerNewRole(pydantic.BaseModel):
    """
    Serializer for NewRole handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    object_id: str = pydantic.Field(
        alias="object_id",
    )
    object_type: typing_extensions.Literal[
        "api_project", "doc_project", "organization"
    ] = pydantic.Field(
        alias="object_type",
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
    user_id: str = pydantic.Field(
        alias="user_id",
    )
