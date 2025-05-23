from openai import AzureOpenAI
from openai import AsyncAzureOpenAI

from src.core.settings import Settings

class AzureClient:

    st = Settings()

    @classmethod
    def openai_client(cls) -> AzureOpenAI:
        """Azure OpenAI Client"""
        return AzureOpenAI(
            azure_endpoint = str(cls.st.azure_openai.endpoint),
            api_key        = cls.st.azure_openai.api_key,
            api_version    = cls.st.azure_openai.api_version
        )
    
    @classmethod
    def async_openai_client(cls) -> AsyncAzureOpenAI:
        """Async Azure OpenAI Client"""
        return AsyncAzureOpenAI(
            azure_endpoint = cls.st.azure_openai.endpoint,
            api_key        = cls.st.azure_openai.api_key,
            api_version    = cls.st.azure_openai.api_version
        )