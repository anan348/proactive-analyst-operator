import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

@dataclass
class AzureOpenAISettings:
    endpoint   : Optional[str] = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key    : Optional[str] = os.getenv('AZURE_OPENAI_API_KEY')
    api_version: Optional[str] = os.getenv('AZURE_OPENAI_API_VERSION')

@dataclass
class Settings:
    azure_openai: AzureOpenAISettings = field(default_factory=AzureOpenAISettings)