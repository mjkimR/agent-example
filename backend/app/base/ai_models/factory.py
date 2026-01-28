import os
import re
from typing import Any, TYPE_CHECKING
from functools import lru_cache
from threading import Lock

import yaml

from app.base.ai_models.schemas import AIModelCatalogItem, AIModelGroupCatalogItem, AIModelType, AICatalogItem
from app.core.config import get_app_path
from app.core.logger import logger
from app.base.ai_models.factory_embedding import EmbeddingFactory
from app.base.ai_models.factory_llm import LLMFactory

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from langchain_core.embeddings import Embeddings


class ConfigLoader:
    @staticmethod
    def load_yaml_with_env(path: str) -> dict[str, Any]:
        pattern = re.compile(r'\$\{(\w+)}')

        def replace_env(match):
            env_var = match.group(1)
            # If the environment variable does not exist, leave as is (or you can raise an error)
            return os.environ.get(env_var, match.group(0))

        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = pattern.sub(replace_env, content)
            return yaml.safe_load(content)


class AIModelFactory:
    _instance = None
    _lock = Lock()
    DEFAULT_PATH = os.path.join(get_app_path(), "catalog.yml")

    def __new__(cls, config_path: str = DEFAULT_PATH):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AIModelFactory, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = DEFAULT_PATH):
        if getattr(self, "_initialized", False):
            return

        logger.info(f"[System] Loading Catalog from {config_path}...")
        raw_config = ConfigLoader.load_yaml_with_env(config_path)

        self.catalog: dict[str, AIModelCatalogItem] = {}
        self.groups: dict[str, AIModelGroupCatalogItem] = {}
        for item in raw_config.get('catalog', []):
            if "name" not in item:
                raise ValueError("Each catalog item must have a 'name' field.")
            name = item["name"]
            try:
                self.catalog[name] = AIModelCatalogItem(**item)
            except Exception as e:
                raise ValueError(f"Error in catalog item '{name}': {str(e)}") from e
        for item in raw_config.get('groups', []):
            if "name" not in item:
                raise ValueError("Each group item must have a 'name' field.")
            name = item["name"]
            try:
                self.groups[name] = AIModelGroupCatalogItem(**item)
            except Exception as e:
                raise ValueError(f"Error in group item '{name}': {str(e)}") from e

        self._validate_config()

        self.llm_factory = LLMFactory()
        self.embedding_factory = EmbeddingFactory()

        self._config_path = config_path  # Save path for reload
        self._initialized = True

    def _validate_config(self):
        """Validate the integrity and type correctness of the configuration file."""
        # 1. Group Item Validation
        for name, group in self.groups.items():
            # (5) Circular Group target Check & Final Target Resolution
            visited = set()
            current_target_name = group.target
            path = [name]
            while current_target_name in self.groups:
                if current_target_name in visited:
                    raise ValueError(f"Configuration Error: Circular reference detected in group target chain: {' -> '.join(path)}")
                visited.add(current_target_name)
                path.append(current_target_name)
                current_target_name = self.groups[current_target_name].target

            resolved_target_name = current_target_name

            # (1) Target Existence Check
            if resolved_target_name not in self.catalog:
                raise ValueError(f"Configuration Error: Group '{name}' refers to non-existent target '{resolved_target_name}'.")

            # (2) Type Consistency Check (Group Type vs Target Type)
            group_type = group.type
            target_type = self.catalog[resolved_target_name].type
            if group_type != target_type:
                raise ValueError(f"Configuration Error: Group '{name}' type ({group_type.value}) does not match final target '{resolved_target_name}' type ({target_type.value}).")

            # (3) Fallback Validation
            for fb_name in group.fallbacks:
                if fb_name in self.catalog:
                    fb_type = self.catalog[fb_name].type
                elif fb_name in self.groups:
                    fb_type = self.groups[fb_name].type
                else:
                    raise ValueError(f"Configuration Error: Group '{name}' has fallback to non-existent model/group '{fb_name}'.")
                if group_type != fb_type:
                    raise ValueError(f"Configuration Error: Group '{name}' fallback '{fb_name}' type ({fb_type.value}) does not match group type ({group_type.value}).")

            # (4) Self-referential Fallback Check
            if name in group.fallbacks:
                raise ValueError(f"Configuration Error: Group '{name}' cannot have itself as a fallback.")

        # 2. Name Conflict Check
        catalog_names = set(self.catalog.keys())
        group_names = set(self.groups.keys())
        conflicts = catalog_names.intersection(group_names)
        if conflicts:
            raise ValueError(f"Configuration Error: Model names must be unique. Conflicts found: {conflicts}")

    @lru_cache(maxsize=32)
    def _get_llm(self, name: str) -> 'BaseChatModel':
        config = self._resolve_config(name, AIModelType.LLM)
        return self.llm_factory.create_model(config.model_dump(exclude_unset=True))

    def get_llm(self, name: str, **kwargs) -> 'BaseChatModel':
        """
        LRU Cache applied:
        If the same 'name' is requested, returns the cached object instead of executing the function
        Returns the LLM model instance for the given name, with optional parameter binding.

        Example:
            llm = model_factory.get_llm("gpt-4", temperature=0.5)

        [Note]
        - Fallback models are NOT included here. Use `get_fallback_llms` to get them if needed. (model.with_fallbacks() is not a BaseChatModel)
        """
        model = self._get_llm(name)
        if kwargs:
            model = model.bind(**kwargs)
        return model

    def get_fallback_llms(self, name: str) -> list['BaseChatModel']:
        """
        [Helper] Returns the list of fallback models configured for this model.

        [Note]
        - Only one-level fallback is supported; multi-level fallback chains are not supported.
        """
        if name in self.groups:
            config = self.groups[name]
            # Verify the group is an LLM group
            if config.type != AIModelType.LLM:
                raise ValueError(
                    f"Type mismatch: Group '{name}' is type '{config.type.value}', but LLM fallbacks were requested."
                )
        elif name in self.catalog:
            # A base model can also have fallbacks defined.
            config = self.catalog[name]
            if config.type != AIModelType.LLM:
                raise ValueError(
                    f"Type mismatch: Model '{name}' is type '{config.type.value}', but LLM fallbacks were requested."
                )
        else:
            raise ValueError(f"Model or group '{name}' not found in catalog or groups.")

        fallback_models = []
        for fb_name in config.fallbacks:
            fallback_models.append(self.get_llm(fb_name))

        return fallback_models

    @lru_cache(maxsize=8)
    def _get_embedding(self, name: str) -> 'Embeddings':
        config = self._resolve_config(name, AIModelType.EMBEDDING)
        return self.embedding_factory.create_model(config.model_dump(exclude_unset=True))

    def get_embedding(self, name: str) -> 'Embeddings':
        model = self._get_embedding(name)
        return model

    def _resolve_config(self, name: str, expected_type: AIModelType | str | None = None) -> AIModelCatalogItem:
        """Name resolution"""
        # 1. Group Resolution (If name is a group, resolve to target model)
        while name in self.groups:
            group = self.groups[name]
            name = group.target

        # 2. Existence Check
        if name not in self.catalog:
            raise ValueError(f"Model '{name}' not found in catalog.")

        config = self.catalog[name]

        # 3. Usage Check
        if expected_type:
            req_type = AIModelType(expected_type) if isinstance(expected_type, str) else expected_type
            actual_type = config.type
            if actual_type != req_type:
                raise ValueError(
                    f"Type mismatch: Requested model '{name}' is '{actual_type.value}', "
                    f"but operation expects '{req_type.value}'."
                )

        return config

    def reload(self):
        """When the config file changes, clear the cache and reload"""
        logger.info("[System] Reloading Catalog...")
        self._get_llm.cache_clear()
        self._get_embedding.cache_clear()
        self._initialized = False
        self.__init__(self._config_path)

    def get_catalog(self, model_type: AIModelType | str) -> list[AICatalogItem]:
        target_type = AIModelType(model_type) if isinstance(model_type, str) else model_type
        results: list[AICatalogItem] = []

        # 1. Catalog
        for name, info in self.catalog.items():
            if info.type == target_type:
                results.append(info.to_catalog_item())

        # 2. Groups
        for name, info in self.groups.items():
            if info.type == target_type:
                results.append(info.to_catalog_item())

        return sorted(results, key=lambda x: (x.kind == "group", x.provider, x.name))
