from workflow.state import AgentState

class PaymentNode:
    @staticmethod
    def verify(state: AgentState) -> AgentState:
        """Verify payment node"""
        if not state.get("tx_hash"):
            state["metrics"].status = "failed"
            state["metrics"].error = "Missing transaction hash"
            return {"payment_verified": False, "error": "No transaction hash"}
        
        print("Payment verified!")
        state["metrics"].status = "verified"
        return {"payment_verified": True}
    
    @staticmethod
    def handle_failure(state: AgentState) -> AgentState:
        """Handle payment failure node"""
        from core.metrics.reporting import MonitoringDashboard
        
        state["metrics"].status = "failed"
        MonitoringDashboard.log_transaction(
            state.get("tx_hash", "failed_tx"),
            state["metrics"]
        )
        return {"error": state.get("error", "Payment failed")}