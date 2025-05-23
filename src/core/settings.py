import os

from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AzureOpenAISettings:
    endpoint   : str = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key    : str = os.getenv('AZURE_OPENAI_API_KEY')
    api_version: str = os.getenv('AZURE_OPENAI_API_VERSION')

@dataclass
class Settings:
    azure_openai: AzureOpenAISettings = AzureOpenAISettings()