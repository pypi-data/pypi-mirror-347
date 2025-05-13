import pydantic
import typing


class DocProjectActionButton(pydantic.BaseModel):
    """
    DocProjectActionButton
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    enabled: bool = pydantic.Field(
        alias="enabled",
    )
    label: typing.Optional[str] = pydantic.Field(
        alias="label",
    )
    url: typing.Optional[str] = pydantic.Field(
        alias="url",
    )
