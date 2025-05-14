import pydantic

from .doc_project_domains import DocProjectDomains
from .doc_project_logos import DocProjectLogos
from .doc_project_settings import DocProjectSettings
from .doc_version import DocVersion


class DocProject(pydantic.BaseModel):
    """
    DocProject
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    created_at: str = pydantic.Field(
        alias="created_at",
    )
    current_version: DocVersion = pydantic.Field(
        alias="current_version",
    )
    domains: DocProjectDomains = pydantic.Field(
        alias="domains",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    logos: DocProjectLogos = pydantic.Field(
        alias="logos",
    )
    name: str = pydantic.Field(
        alias="name",
    )
    settings: DocProjectSettings = pydantic.Field(
        alias="settings",
    )
