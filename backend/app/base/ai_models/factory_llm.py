from typing import TYPE_CHECKING

from app.base.ai_models.schemas import AIModelCatalogItem

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class LLMFactory:
    def create_model(self, config: AIModelCatalogItem) -> 'BaseChatModel':
        provider = config.provider
        args = config.args

        try:
            match provider:
                case 'openai-compatible' | 'openai':
                    from langchain_openai import ChatOpenAI
                    return ChatOpenAI(**args)
                case 'google':
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    if 'api_key' in args:
                        args['google_api_key'] = args.pop('api_key')
                    return ChatGoogleGenerativeAI(**args)
                case _:
                    raise ValueError(f"Unsupported LLM provider: {provider}")
        except ImportError as e:
            raise ImportError(
                f"Failed to import dependencies for provider '{provider}'. "
                f"Please install the required package (e.g., pip install '.[{provider}]'). Original error: {e}"
            )
