import pydantic
import typing
import typing_extensions


class NewDeployment(typing_extensions.TypedDict):
    """
    NewDeployment
    """

    doc_version_id: typing_extensions.NotRequired[str]

    target: typing_extensions.Required[
        typing_extensions.Literal["Preview", "Production"]
    ]


class _SerializerNewDeployment(pydantic.BaseModel):
    """
    Serializer for NewDeployment handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    doc_version_id: typing.Optional[str] = pydantic.Field(
        alias="doc_version_id", default=None
    )
    target: typing_extensions.Literal["Preview", "Production"] = pydantic.Field(
        alias="target",
    )
