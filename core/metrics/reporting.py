from datetime import datetime
import pandas as pd
from core.metrics.tracker import PerformanceMetrics

class MonitoringDashboard:
    transactions = {}
    
    @classmethod
    def log_transaction(cls, tx_hash: str, metrics: PerformanceMetrics):
        """Log a transaction with its metrics"""
        cls.transactions[tx_hash] = {
            "timestamp": datetime.now().isoformat(),
            "tokens": metrics.tokens_used,
            "cost": metrics.cost_usdc,
            "status": metrics.status,
            "duration": metrics.calculate_duration(),
            "error": metrics.error
        }
    
    @classmethod
    def generate_report(cls):
        """Generate a performance report"""
        df = pd.DataFrame(cls.transactions.values())
        if df.empty:
            return {"status": "No transactions yet"}
        
        success_count = len(df[df.status == "delivered"])
        return {
            "total_transactions": len(df),
            "success_rate": f"{success_count/len(df)*100:.1f}%" if len(df) > 0 else "0%",
            "avg_cost": f"${df.cost.mean():.6f}" if len(df) > 0 else "$0.000000",
            "avg_tokens": int(df.tokens.mean()) if len(df) > 0 else 0,
            "avg_duration": f"{df.duration.mean():.2f}s" if len(df) > 0 else "0.00s"
        }