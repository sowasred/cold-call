from enum import Enum
import os
from crewai import LLM

class LLMProvider(Enum):
    DEEPSEEK = "DEEPSEEK"
    OPENAI = "OPENAI"
    OLLAMA = "OLLAMA"

def initialize_llm(provider: LLMProvider) -> LLM:
    """Initialize LLM based on the selected provider.
    
    Args:
        provider: The LLM provider to use
            
    Returns:
        LLM: Initialized LLM instance
        
    Raises:
        ValueError: If provider is invalid or env vars are missing
    """
    llm_configs = {
        LLMProvider.DEEPSEEK: {
            "model": f"deepseek/{os.getenv('DEEPSEEK_MODEL')}",
            "base_url": os.getenv('DEEPSEEK_BASE_URL'),
            "api_key": os.getenv('DEEPSEEK_API_KEY'),
            "messages": [
                {"role": "user", "content": "Finish the given task"},
                {"role": "assistant", "content": "I'll finish the task."}
            ],
            "temperature": 0.7
        },
        LLMProvider.OPENAI: {
            "model": os.getenv('OPENAI_MODEL'),
            "base_url": os.getenv('OPENAI_BASE_URL'),
            "api_key": os.getenv('OPENAI_API_KEY')
        },
        LLMProvider.OLLAMA: {
            "model": f"ollama/{os.getenv('OLLAMA_MODEL')}",
            "base_url": os.getenv('OLLAMA_BASE_URL')
        }
    }
    
    if provider not in llm_configs:
        raise ValueError(f"Unsupported LLM provider: {provider}")
        
    config = llm_configs[provider]
    if any(value is None for value in config.values()):
        raise ValueError(f"Missing required environment variables for {provider.value}")
        
    return LLM(**config) 