import pydantic
import typing

from .asset import Asset
from .pagination import Pagination


class ListAssetsPage(pydantic.BaseModel):
    """
    ListAssetsPage
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    pagination: Pagination = pydantic.Field(
        alias="pagination",
    )
    results: typing.List[Asset] = pydantic.Field(
        alias="results",
    )
