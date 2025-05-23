from typing import Optional

from dataclasses import dataclass
from agents import OpenAIChatCompletionsModel

from src.integration.azure.client import AzureClient

@dataclass
class ModelConfiguration:
    model_name: str
    # TODO: max_tokenとかはここにいれる？

    @classmethod
    def default(cls) -> 'ModelConfiguration':
        return cls(model_name='gpt-4o-mini')
    

class ModelFactory:

    _model_cache: dict[str, OpenAIChatCompletionsModel] = {}


    @classmethod
    def create_openai_model(
        cls,
        model_name: str,
        use_cache : bool = True
    ) -> OpenAIChatCompletionsModel:
        """OpenAIモデルを生成する"""

        # キャッシュを使用し、キャッシュに存在する場合はそれを返す
        if model_name in cls._model_cache:
            return cls._model_cache[model_name]
        
        azure_client = AzureClient.async_openai_client()
        model = OpenAIChatCompletionsModel(
            model         = model_name,
            openai_client = azure_client
        )

        if use_cache:
            cls._model_cache[model_name] = model

        return model
    
    @classmethod
    def create_from_config(cls, config: ModelConfiguration, use_cache: bool = True) -> OpenAIChatCompletionsModel:
        """モデルを生成する"""
        return cls.create_openai_model(
            model_name = config.model_name,
            use_cache  = use_cache
        )
    
    @classmethod
    def get_default_model(cls) -> OpenAIChatCompletionsModel:
        """デフォルトのモデルを取得する"""
        return cls.create_from_config(config = ModelConfiguration.default())