import pydantic


class ModuleDoc(pydantic.BaseModel):
    """
    ModuleDoc
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    content: str = pydantic.Field(
        alias="content",
    )
    """
    Markdown content with documentation for the module
    """
    module: str = pydantic.Field(
        alias="module",
    )
    """
    Module name/identifier
    """
