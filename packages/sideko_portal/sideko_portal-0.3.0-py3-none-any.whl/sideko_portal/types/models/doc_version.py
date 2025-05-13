import pydantic
import typing_extensions


class DocVersion(pydantic.BaseModel):
    """
    DocVersion
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    created_at: str = pydantic.Field(
        alias="created_at",
    )
    doc_project_id: str = pydantic.Field(
        alias="doc_project_id",
    )
    id: str = pydantic.Field(
        alias="id",
    )
    status: typing_extensions.Literal["Draft", "Published", "Publishing"] = (
        pydantic.Field(
            alias="status",
        )
    )
    version: int = pydantic.Field(
        alias="version",
    )
