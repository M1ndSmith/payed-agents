from typing import TypedDict, Optional
from core.metrics.tracker import PerformanceMetrics

class AgentState(TypedDict):
    data_request: Optional[str]
    tx_hash: Optional[str]
    payment_verified: Optional[bool]
    data: Optional[dict]
    error: Optional[str]
    consumer_wallet: Optional[object]
    provider_wallet: Optional[object]
    token_usage: Optional[int]
    calculated_cost: Optional[float]
    metrics: Optional[PerformanceMetrics]
    initial_response: Optional[str]