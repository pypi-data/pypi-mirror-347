import pydantic
import typing_extensions


class SdkGeneration(pydantic.BaseModel):
    """
    SdkGeneration
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    api_version_id: str = pydantic.Field(
        alias="api_version_id",
    )
    created_at: str = pydantic.Field(
        alias="created_at",
    )
    language: typing_extensions.Literal[
        "go", "java", "python", "rust", "typescript"
    ] = pydantic.Field(
        alias="language",
    )
    """
    Programming languages available for SDK generation
    """
    name: str = pydantic.Field(
        alias="name",
    )
    """
    Package name of generated sdks
    """
    successful: bool = pydantic.Field(
        alias="successful",
    )
    version: str = pydantic.Field(
        alias="version",
    )
    """
    Semantic version following conventions from https://semver.org/
    """
