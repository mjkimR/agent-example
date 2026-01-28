from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class AIModelType(str, Enum):
    LLM = "llm"
    EMBEDDING = "text-embedding"
    STT = "stt"
    TTS = "tts"
    IMAGE_GEN = "image-generation"


class AICatalogItem(BaseModel):
    name: str = Field(..., description="The name of the model or alias")
    kind: Literal["model", "alias"] = Field(..., description="Indicates whether this is a model or alias")
    type: AIModelType = Field(..., description="The type of the model")
    help: str | None = Field(default=None, description="Description of the model or alias")
    provider: str | None = Field(default=None, description="The provider of the model (provider is 'alias' for aliases)")


class AIModelItem(BaseModel):
    name: str = Field(..., description="The name of the model")
    type: AIModelType = Field(..., description="The type of the model")
    provider: str = Field(..., description="The provider of the model")
    help: str | None = Field(default=None, description="Description of the model")
    args: dict[str, Any] = Field(default_factory=dict, description="Arguments for model initialization")
    fallbacks: list[str] = Field(default_factory=list, description="List of fallback model/alias names")
    kind: Literal["model"] = Field(default="model", description="Indicates this is a model item")

    def to_catalog_item(self) -> AICatalogItem:
        return AICatalogItem(
            name=self.name,
            kind="model",
            type=self.type,
            help=self.help,
            provider=self.provider,
        )


class AIModelAliasItem(BaseModel):
    name: str = Field(..., description="The name of the model alias")
    type: AIModelType = Field(..., description="The type of models in this alias")
    target: str = Field(..., description="The target model name for this alias")
    help: str | None = Field(default=None, description="Description of the model alias")
    fallbacks: list[str] = Field(default_factory=list, description="List of fallback model/alias names")
    kind: Literal["alias"] = Field(default="alias", description="Indicates this is an alias item")

    def to_catalog_item(self) -> AICatalogItem:
        base_desc = self.help or 'Model Alias'
        full_desc = f"{base_desc} (Target: {self.target})"

        return AICatalogItem(
            name=self.name,
            type=self.type,
            provider="alias",
            help=full_desc,
            kind="alias",
        )
