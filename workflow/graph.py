from langgraph.graph import StateGraph, END
from workflow.state import AgentState
from workflow.nodes import WorkflowNodes

class WorkflowGraph:
    def __init__(self, llm):
        self.nodes = WorkflowNodes(llm)
        self.chain = None
    
    def build(self):
        """Build workflow graph"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("consumer", self.nodes.consumer_agent)
        workflow.add_node("verify_payment", self.nodes.verify_payment)
        workflow.add_node("provider", self.nodes.provider_agent)
        workflow.add_node("deliver_data", self.nodes.deliver_data)
        workflow.add_node("handle_failure", self.nodes.payment_failure)
        
        # Define edges
        workflow.set_entry_point("consumer")
        workflow.add_edge("consumer", "verify_payment")
        workflow.add_conditional_edges(
            "verify_payment",
            lambda s: "provider" if s.get("payment_verified") else "handle_failure",
            {"provider": "provider", "handle_failure": "handle_failure"}
        )
        workflow.add_edge("provider", "deliver_data")
        workflow.add_edge("deliver_data", END)
        workflow.add_edge("handle_failure", END)
        
        # Compile the workflow
        self.chain = workflow.compile()
        return self.chain
    
    def execute(self, state):
        """Execute the workflow with given state"""
        if not self.chain:
            raise ValueError("Workflow not built. Call build() first.")
        return self.chain.invoke(state)