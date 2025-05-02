from workflow.state import AgentState

class ProviderNode:
    @staticmethod
    def process(state: AgentState) -> AgentState:
        """Provider agent node"""
        if not state.get("payment_verified"):
            state["metrics"].status = "failed"
            state["metrics"].error = "Payment not verified"
            return {"error": "Payment not verified"}
        
        try:
            print("Processing response...")
            
            # Check if an agent has already processed the query
            if "agent_result" in state and state["agent_result"]["success"]:
                print("Using pre-processed agent result...")
                agent_result = state["agent_result"]
                
                # Use the agent result and add payment-related information
                state["metrics"].status = "processed_by_agent"
                state["metrics"].agent_name = agent_result["agent"]
                
                # Estimate token usage and cost
                # In a real scenario, this would be calculated based on the agent's actual usage
                state["token_usage"] = {"input": 250, "output": 750, "total": 1000}  # Simplified estimate
                state["calculated_cost"] = 0.002  # Fixed cost for agent processing
                
                return {
                    **state,
                    "data": {"content": agent_result["content"]},
                    "token_usage": state["token_usage"],
                    "calculated_cost": state["calculated_cost"]
                }
            else:
                # Standard LLM processing without agent
                state["metrics"].status = "processed"
                return {
                    **state,
                    "data": {"content": state["initial_response"]},
                    "token_usage": state["token_usage"],
                    "calculated_cost": state["calculated_cost"]
                }
        except Exception as e:
            state["metrics"].status = "failed"
            state["metrics"].error = str(e)
            return {"error": f"Processing failed: {str(e)}"}