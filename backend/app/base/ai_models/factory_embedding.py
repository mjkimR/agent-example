from typing import TYPE_CHECKING

from app.base.ai_models.schemas import AIModelItem

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings


class EmbeddingFactory:
    def create_model(self, config: AIModelItem) -> 'Embeddings':
        provider = config.provider
        args = config.args

        try:
            match provider:
                case 'openai-compatible' | 'openai':
                    from langchain_openai import OpenAIEmbeddings
                    return OpenAIEmbeddings(**args)
                case 'google':
                    from langchain_google_genai import GoogleGenerativeAIEmbeddings
                    if 'api_key' in args:
                        args['google_api_key'] = args.pop('api_key')
                    return GoogleGenerativeAIEmbeddings(**args)
                case _:
                    raise ValueError(f"Unsupported Embedding provider: {provider}")
        except ImportError as e:
            raise ImportError(
                f"Failed to import dependencies for provider '{provider}'. "
                f"Please install the required package. Original error: {e}"
            )
