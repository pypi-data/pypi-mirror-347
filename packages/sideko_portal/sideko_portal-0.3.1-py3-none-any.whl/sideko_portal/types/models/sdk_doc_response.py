import pydantic
import typing

from .module_doc import ModuleDoc


class SdkDocResponse(pydantic.BaseModel):
    """
    SdkDocResponse
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    client_init: str = pydantic.Field(
        alias="client_init",
    )
    """
    Client initialization code
    """
    modules: typing.List[ModuleDoc] = pydantic.Field(
        alias="modules",
    )
    """
    Array of module documentation objects
    """
