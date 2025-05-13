import pydantic
import typing
import typing_extensions

from .update_doc_project_settings_action_button import (
    UpdateDocProjectSettingsActionButton,
    _SerializerUpdateDocProjectSettingsActionButton,
)
from .update_doc_project_settings_metadata import (
    UpdateDocProjectSettingsMetadata,
    _SerializerUpdateDocProjectSettingsMetadata,
)


class UpdateDocProjectSettings(typing_extensions.TypedDict):
    """
    UpdateDocProjectSettings
    """

    action_button: typing_extensions.NotRequired[UpdateDocProjectSettingsActionButton]

    metadata: typing_extensions.NotRequired[UpdateDocProjectSettingsMetadata]


class _SerializerUpdateDocProjectSettings(pydantic.BaseModel):
    """
    Serializer for UpdateDocProjectSettings handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    action_button: typing.Optional[_SerializerUpdateDocProjectSettingsActionButton] = (
        pydantic.Field(alias="action_button", default=None)
    )
    metadata: typing.Optional[_SerializerUpdateDocProjectSettingsMetadata] = (
        pydantic.Field(alias="metadata", default=None)
    )
