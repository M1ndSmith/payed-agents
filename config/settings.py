class LLMSettings:
    PROVIDER = "groq"  # Default provider: groq, anthropic, openai, deepseek
    MODEL_NAME = "llama3-8b-8192"
    MAX_TOKENS = 8192
    TEMPERATURE = 0.7

class WalletSettings:
    CONSUMER_WALLET_ID = '3e4c9f11-18a3-4905-a474-777909c5736d'
    PROVIDER_WALLET_ID = 'e5b34cf5-df25-4ceb-8b81-8d0036f7d8ef'
    ASSET_ID = "usdc"
    GASLESS = False