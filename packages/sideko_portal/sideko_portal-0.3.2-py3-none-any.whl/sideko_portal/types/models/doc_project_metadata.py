import pydantic
import typing


class DocProjectMetadata(pydantic.BaseModel):
    """
    DocProjectMetadata
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    description: typing.Optional[str] = pydantic.Field(
        alias="description",
    )
    title: typing.Optional[str] = pydantic.Field(
        alias="title",
    )
