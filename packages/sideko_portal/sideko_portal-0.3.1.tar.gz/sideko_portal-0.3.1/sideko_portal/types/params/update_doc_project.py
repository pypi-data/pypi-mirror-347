import pydantic
import typing
import typing_extensions

from .update_doc_project_logos import (
    UpdateDocProjectLogos,
    _SerializerUpdateDocProjectLogos,
)
from .update_doc_project_settings import (
    UpdateDocProjectSettings,
    _SerializerUpdateDocProjectSettings,
)


class UpdateDocProject(typing_extensions.TypedDict):
    """
    UpdateDocProject
    """

    logos: typing_extensions.NotRequired[UpdateDocProjectLogos]

    name: typing_extensions.NotRequired[str]

    settings: typing_extensions.NotRequired[UpdateDocProjectSettings]


class _SerializerUpdateDocProject(pydantic.BaseModel):
    """
    Serializer for UpdateDocProject handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    logos: typing.Optional[_SerializerUpdateDocProjectLogos] = pydantic.Field(
        alias="logos", default=None
    )
    name: typing.Optional[str] = pydantic.Field(alias="name", default=None)
    settings: typing.Optional[_SerializerUpdateDocProjectSettings] = pydantic.Field(
        alias="settings", default=None
    )
