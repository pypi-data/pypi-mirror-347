import pydantic

from .organization import Organization


class OrganizationWithRedirect(pydantic.BaseModel):
    """
    OrganizationWithRedirect
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    organization: Organization = pydantic.Field(
        alias="organization",
    )
    redirect_to: str = pydantic.Field(
        alias="redirect_to",
    )
