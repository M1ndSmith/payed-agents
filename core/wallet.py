from cdp import Wallet, Cdp
from config.settings import WalletSettings

class WalletManager:
    @staticmethod
    def initialize_cdp(api_key_path):
        """Initialize CDP with API key"""
        try:
            Cdp.configure_from_json(api_key_path)
            return True
        except Exception as e:
            print(f"CDP initialization failed: {str(e)}")
            return False
    
    @staticmethod
    def import_wallet(wallet_id, seed_file):
        """Import an existing wallet"""
        try:
            wallet = Wallet.fetch(wallet_id)
            wallet.load_seed_from_file(seed_file)
            print(f"  Imported wallet: {wallet_id}")
            wallet.addresses  # Fetch addresses
            return wallet
        except Exception as e:
            print(f"  Failed to import wallet: {str(e)}")
            return None
    
    @classmethod
    def import_consumer_wallet(cls, seed_file):
        """Import consumer wallet using predefined ID"""
        return cls.import_wallet(WalletSettings.CONSUMER_WALLET_ID, seed_file)
    
    @classmethod
    def import_provider_wallet(cls, seed_file):
        """Import provider wallet using predefined ID"""
        return cls.import_wallet(WalletSettings.PROVIDER_WALLET_ID, seed_file)