from enum import Enum
from typing import Dict, Any, Optional
import yaml
import os
from crewai import LLM
class LLMProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

class LLMConfig:
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or LLMProvider.OPENAI

    def get_llm(self) -> list:
        """Get llm based on provider"""
        if self.provider == LLMProvider.OLLAMA:
            return LLM(
                model="ollama/llama3.2",
                base_url="http://localhost:11434"
            )
        return []
