import os
from dataclasses import dataclass

@dataclass
class Paths:
    cdp_api: str = "api-key/cdp_api_key.json"
    consumer_seed: str = "wallets/consumer_seed.json"
    provider_seed: str = "wallets/provider_seed.json"
    
    @classmethod
    def validate(cls, paths):
        """Validate that all paths exist"""
        for name, path in vars(paths).items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path does not exist: {path} ({name})")
        return True