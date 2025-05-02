from pprint import pprint
import json

class OutputFormatter:
    @staticmethod
    def print_transaction_details(tx_hash, cost, tokens):
        """Print transaction details"""
        print("\n--- Transaction Details ---")
        print(f"Transaction Hash: {tx_hash}")
        print(f"Cost: {cost:.6f} USDC")
        print(f"Tokens used: {tokens}")
    
    @staticmethod
    def print_response_content(content):
        """Print response content"""
        print("\n--- Response Content ---\n")
        print(content)
    
    @staticmethod
    def print_error(error):
        """Print error message"""
        print(f"\n❌ Error: {error}")
    
    @staticmethod
    def print_report(report):
        """Print monitoring report"""
        print("\n=== Performance Report ===")
        pprint(report)
    
    @staticmethod
    def print_transactions(transactions):
        """Print transaction history"""
        print("\n=== Recent Transactions ===")
        if not transactions:
            print("No transactions recorded.")
        else:
            for tx_hash, data in transactions.items():
                print(f"\nTransaction: {tx_hash[:10]}...")
                print(f"  Status: {data['status']}")
                print(f"  Time: {data['timestamp']}")
                print(f"  Tokens: {data['tokens']}")
                print(f"  Cost: {data['cost']:.6f} USDC")
                if data.get('error'):
                    print(f"  Error: {data['error']}")
    
    @staticmethod
    def export_report(report, transactions, filename="cdp_report.json"):
        """Export report and transactions to JSON file"""
        data = {
            "report": report,
            "transactions": transactions
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nReport exported to {filename}")