from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel

from moxn_models.blocks.image import ImageContentFromSourceModel
from moxn_models.blocks.text import TextContentModel

T = TypeVar("T")


class ToolCallModel(BaseModel):
    id: str
    arguments: str | dict[str, Any] | None
    name: str


class ToolResultBase(BaseModel, Generic[T]):
    type: Literal["tool_use"]
    id: str
    name: str
    content: T | None


class ToolResultModel(
    ToolResultBase[TextContentModel | ImageContentFromSourceModel | None]
):
    type: Literal["tool_use"]
    id: str
    name: str
    content: TextContentModel | ImageContentFromSourceModel | None
