from workflow.state import AgentState
from core.metrics.reporting import MonitoringDashboard

class DeliveryNode:
    @staticmethod
    def deliver(state: AgentState) -> AgentState:
        """Deliver data node"""
        print("Delivering response...")
        state["metrics"].status = "delivered"
        MonitoringDashboard.log_transaction(state["tx_hash"], state["metrics"])
        
        result = {
            "data": state["data"],
            "tx_hash": state["tx_hash"],
            "token_usage": state["token_usage"],
            "calculated_cost": state["calculated_cost"],
            "consumer_wallet": state.get("consumer_wallet"),
            "provider_wallet": state.get("provider_wallet")
        }
        return result