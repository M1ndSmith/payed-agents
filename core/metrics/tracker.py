from dataclasses import dataclass
import time

@dataclass
class PerformanceMetrics:
    start_time: float
    tokens_used: int = 0
    cost_usdc: float = 0.0
    status: str = "pending"
    error: str = None
    
    def calculate_duration(self):
        """Calculate duration in seconds"""
        return time.time() - self.start_time