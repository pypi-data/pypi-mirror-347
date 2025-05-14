import pydantic

from .organization_features import OrganizationFeatures


class Organization(pydantic.BaseModel):
    """
    Organization
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    features: OrganizationFeatures = pydantic.Field(
        alias="features",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    name: str = pydantic.Field(
        alias="name",
    )
    subdomain: str = pydantic.Field(
        alias="subdomain",
    )
