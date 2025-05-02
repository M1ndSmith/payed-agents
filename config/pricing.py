class PricingConfig:
    COST_PER_TOKEN = 0.000001  # $0.000001 per token
    MINIMUM_FEE = 0.00001      # $0.00001 minimum
    
    @classmethod
    def calculate_cost(cls, tokens):
        """Calculate cost based on token count"""
        return max(tokens * cls.COST_PER_TOKEN, cls.MINIMUM_FEE)