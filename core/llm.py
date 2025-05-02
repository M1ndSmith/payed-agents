from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from config.settings import LLMSettings
from config.yaml_config import ConfigLoader

class LLMProvider:
    @staticmethod
    def create_llm(provider=None, model_name=None, config_path='config.yaml'):
        """Create LLM instance with optional provider and model override"""
        try:
            # Get provider from args, or from YAML config, or fallback to settings
            provider = provider or ConfigLoader.get_llm_provider(config_path) or LLMSettings.PROVIDER
            
            # Get model from args, or from YAML config for the provider, or fallback to settings
            if model_name is None:
                model_name = ConfigLoader.get_llm_model(provider, config_path) or LLMSettings.MODEL_NAME
            
            print(f"Initializing {provider} LLM with model: {model_name}")
            
            if provider == "groq":
                return ChatGroq(
                    model=model_name,
                    temperature=LLMSettings.TEMPERATURE,
                    max_tokens=LLMSettings.MAX_TOKENS
                )
            elif provider == "anthropic":
                return ChatAnthropic(
                    model=model_name,
                    temperature=LLMSettings.TEMPERATURE,
                    max_tokens=LLMSettings.MAX_TOKENS
                )
            elif provider == "openai":
                return ChatOpenAI(
                    model=model_name,
                    temperature=LLMSettings.TEMPERATURE,
                    max_tokens=LLMSettings.MAX_TOKENS
                )
            else:
                # Default to Groq
                default_model = ConfigLoader.get_llm_model("groq", config_path) or LLMSettings.MODEL_NAME
                print(f"Unknown provider '{provider}', falling back to groq with model: {default_model}")
                return ChatGroq(
                    model=default_model,
                    temperature=LLMSettings.TEMPERATURE,
                    max_tokens=LLMSettings.MAX_TOKENS
                )
                
        except Exception as e:
            print(f"Failed to initialize LLM: {str(e)}")
            return None
            
    @staticmethod
    def list_available_models(provider=None, config_path='config.yaml'):
        """List available models for a provider"""
        if provider is None:
            provider = ConfigLoader.get_llm_provider(config_path)
        
        return ConfigLoader.get_available_models(provider, config_path)