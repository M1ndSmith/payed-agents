import time
from workflow.state import AgentState
from core.metrics.tracker import PerformanceMetrics
from core.metrics.reporting import MonitoringDashboard
from config.pricing import PricingConfig
from config.settings import WalletSettings

class ConsumerNode:
    def __init__(self, llm):
        self.llm = llm

    def process(self, state: AgentState) -> AgentState:
        """Consumer agent node"""
        if not state.get("data_request"):
            return {"error": "No data request provided"}
        
        metrics = PerformanceMetrics(start_time=state.get("metrics").start_time 
                                    if state.get("metrics") else time.time())
        
        try:
            print("Processing request with LLM...")
            response = self.llm.invoke(state["data_request"])
            tokens = response.response_metadata['token_usage']['completion_tokens']
            cost = PricingConfig.calculate_cost(tokens)
            
            print(f"Sending payment of {cost} USDC...")
            transfer = state["consumer_wallet"].transfer(
                amount=cost,
                asset_id=WalletSettings.ASSET_ID,
                destination=state["provider_wallet"],
                gasless=WalletSettings.GASLESS
            ).wait()
            
            metrics.tokens_used = tokens
            metrics.cost_usdc = cost
            metrics.status = "paid"
            
            return {
                **state,
                "tx_hash": transfer.transaction_hash,
                "token_usage": tokens,
                "calculated_cost": cost,
                "metrics": metrics,
                "initial_response": response.content,
                "payment_verified": None
            }
        except Exception as e:
            metrics.status = "failed"
            metrics.error = str(e)
            MonitoringDashboard.log_transaction("failed_tx", metrics)
            return {"error": f"Payment failed: {str(e)}"}