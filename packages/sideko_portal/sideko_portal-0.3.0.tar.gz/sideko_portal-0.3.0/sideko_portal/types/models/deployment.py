import pydantic
import typing
import typing_extensions

from .doc_version import DocVersion


class Deployment(pydantic.BaseModel):
    """
    Deployment
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    created_at: str = pydantic.Field(
        alias="created_at",
    )
    current_preview: bool = pydantic.Field(
        alias="current_preview",
    )
    current_prod: bool = pydantic.Field(
        alias="current_prod",
    )
    doc_version: DocVersion = pydantic.Field(
        alias="doc_version",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    metadata: typing.Dict[str, typing.Any] = pydantic.Field(
        alias="metadata",
    )
    """
    an object describing the guides, api links, and theming included in the triggered deployment
    """
    status: typing_extensions.Literal[
        "Building", "Cancelled", "Complete", "Created", "Error", "Generated"
    ] = pydantic.Field(
        alias="status",
    )
    target: typing_extensions.Literal["Preview", "Production"] = pydantic.Field(
        alias="target",
    )
