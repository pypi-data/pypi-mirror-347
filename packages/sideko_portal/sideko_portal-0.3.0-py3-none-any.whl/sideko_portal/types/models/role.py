import pydantic
import typing_extensions

from .role_definition import RoleDefinition
from .user import User


class Role(pydantic.BaseModel):
    """
    Role
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    definition: RoleDefinition = pydantic.Field(
        alias="definition",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    object_id: str = pydantic.Field(
        alias="object_id",
    )
    """
    The unique identifier of the Sideko object
    """
    object_type: typing_extensions.Literal[
        "api_project", "doc_project", "organization"
    ] = pydantic.Field(
        alias="object_type",
    )
    """
    The object types that roles can be assigned to.
    """
    user: User = pydantic.Field(
        alias="user",
    )
