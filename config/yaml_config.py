import yaml
import os

class ConfigLoader:
    _config = None
    
    @classmethod
    def load_config(cls, config_path='config.yaml'):
        """Load configuration from YAML file"""
        if cls._config is None or config_path != getattr(cls, '_config_path', None):
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as file:
                        cls._config = yaml.safe_load(file)
                        cls._config_path = config_path
                else:
                    print(f"Warning: Config file not found at {config_path}")
                    cls._config = {}
                    cls._config_path = config_path
            except Exception as e:
                print(f"Error loading config: {str(e)}")
                cls._config = {}
                cls._config_path = config_path
        return cls._config
    
    @classmethod
    def get_llm_provider(cls, config_path='config.yaml'):
        """Get default LLM provider from config"""
        config = cls.load_config(config_path)
        return config.get('llm', {}).get('provider', 'groq')
    
    @classmethod
    def get_llm_model(cls, provider, config_path='config.yaml'):
        """Get default model for a provider from config"""
        config = cls.load_config(config_path)
        return config.get('llm', {}).get('models', {}).get(provider, {}).get('default', None)
    
    @classmethod
    def get_available_models(cls, provider, config_path='config.yaml'):
        """Get available models for a provider from config"""
        config = cls.load_config(config_path)
        return config.get('llm', {}).get('models', {}).get(provider, {}).get('options', [])
    
    @classmethod
    def get_wallet_settings(cls, config_path='config.yaml'):
        """Get wallet settings from config"""
        config = cls.load_config(config_path)
        return config.get('wallet', {})
    
    @classmethod
    def get_paths(cls, config_path='config.yaml'):
        """Get paths from config"""
        config = cls.load_config(config_path)
        return config.get('paths', {})
    
    @classmethod
    def get_default_agent(cls, config_path='config.yaml'):
        """Get default agent from config"""
        config = cls.load_config(config_path)
        return config.get('agents', {}).get('default', 'basic_llm')
    
    @classmethod
    def get_agent_config(cls, agent_name=None, config_path='config.yaml'):
        """Get configuration for a specific agent"""
        config = cls.load_config(config_path)
        
        if agent_name is None:
            agent_name = cls.get_default_agent(config_path)
            
        return config.get('agents', {}).get('definitions', {}).get(agent_name, {})
    
    @classmethod
    def get_available_agents(cls, config_path='config.yaml'):
        """Get list of available agents"""
        config = cls.load_config(config_path)
        return list(config.get('agents', {}).get('definitions', {}).keys()) 