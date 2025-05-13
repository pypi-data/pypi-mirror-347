import pydantic

from .doc_project_action_button import DocProjectActionButton
from .doc_project_metadata import DocProjectMetadata


class DocProjectSettings(pydantic.BaseModel):
    """
    DocProjectSettings
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    action_button: DocProjectActionButton = pydantic.Field(
        alias="action_button",
    )
    metadata: DocProjectMetadata = pydantic.Field(
        alias="metadata",
    )
