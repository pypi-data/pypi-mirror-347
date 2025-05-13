import pydantic
import typing


class DocProjectDomains(pydantic.BaseModel):
    """
    DocProjectDomains
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    preview: typing.Optional[str] = pydantic.Field(
        alias="preview",
    )
    production: typing.Optional[str] = pydantic.Field(
        alias="production",
    )
