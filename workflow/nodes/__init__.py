import time
from workflow.nodes.consumer import ConsumerNode
from workflow.nodes.provider import ProviderNode
from workflow.nodes.payment import PaymentNode
from workflow.nodes.delivery import DeliveryNode

class WorkflowNodes:
    def __init__(self, llm):
        self.consumer = ConsumerNode(llm)
        self.provider = ProviderNode()
        self.payment = PaymentNode()
        self.delivery = DeliveryNode()
    
    def consumer_agent(self, state):
        return self.consumer.process(state)
    
    def verify_payment(self, state):
        return self.payment.verify(state)
    
    def provider_agent(self, state):
        return self.provider.process(state)
    
    def deliver_data(self, state):
        return self.delivery.deliver(state)
    
    def payment_failure(self, state):
        return self.payment.handle_failure(state)