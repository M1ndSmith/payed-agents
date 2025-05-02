import time
from config.paths import Paths
from core.wallet import WalletManager
from core.llm import LLMProvider
from core.agent_manager import AgentManager
from core.metrics.tracker import PerformanceMetrics
from core.metrics.reporting import MonitoringDashboard
from workflow.graph import WorkflowGraph
from cli.output import OutputFormatter

class CDPCliApp:
    def __init__(self, cdp_api_path, consumer_seed_path, provider_seed_path, 
                 llm_provider=None, llm_model=None, agent_name=None, config_path='config.yaml'):
        self.paths = Paths(
            cdp_api=cdp_api_path,
            consumer_seed=consumer_seed_path,
            provider_seed=provider_seed_path
        )
        self.consumer_wallet = None
        self.provider_wallet = None
        self.llm = None
        self.workflow = None
        self.output = OutputFormatter()
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.agent_name = agent_name
        self.config_path = config_path
        self.agent_manager = None
        self.use_agent = agent_name is not None
    
    def initialize(self):
        """Initialize the application"""
        try:
            # Validate paths
            Paths.validate(self.paths)
            
            # Initialize CDP
            print("Initializing CDP...")
            if not WalletManager.initialize_cdp(self.paths.cdp_api):
                return False
            
            # Import wallets
            print("Importing wallets...")
            self.consumer_wallet = WalletManager.import_consumer_wallet(self.paths.consumer_seed)
            self.provider_wallet = WalletManager.import_provider_wallet(self.paths.provider_seed)
            
            if not self.consumer_wallet or not self.provider_wallet:
                return False
            
            # Initialize LLM or Agent based on parameters
            if self.use_agent:
                print(f"Setting up agent: {self.agent_name}...")
                self.agent_manager = AgentManager(config_path=self.config_path)
                # We'll still need an LLM for other parts of the workflow
                # This will be used for non-agent parts of processing
                self.llm = LLMProvider.create_llm(
                    provider=self.llm_provider,
                    model_name=self.llm_model,
                    config_path=self.config_path
                )
            else:
                # Traditional LLM approach
                provider_info = f"{self.llm_provider}" if self.llm_provider else "default"
                model_info = f" with model {self.llm_model}" if self.llm_model else ""
                print(f"Setting up LLM using provider: {provider_info}{model_info}...")
                
                self.llm = LLMProvider.create_llm(
                    provider=self.llm_provider,
                    model_name=self.llm_model,
                    config_path=self.config_path
                )
            
            if not self.llm:
                return False
            
            # Setup workflow
            print("Building workflow...")
            self.workflow = WorkflowGraph(self.llm)
            self.workflow.build()
            
            print("Initialization complete!")
            return True
        except Exception as e:
            print(f"Initialization failed: {str(e)}")
            return False
    
    def process_query(self, query):
        """Process a single query"""
        if not self.workflow:
            print("Workflow not initialized. Run initialize() first.")
            return None
        
        print(f"\n\n=== Processing Query ===\n{query}\n")
        
        # Start timing and metrics
        start_time = time.time()
        metrics = PerformanceMetrics(start_time=start_time)
        
        # If using agent, process with agent first
        agent_result = None
        if self.use_agent and self.agent_manager:
            print(f"Processing with agent: {self.agent_name}...")
            agent_result = self.agent_manager.execute_agent(self.agent_name, query)
            
            if not agent_result['success']:
                print(f"Agent execution failed: {agent_result['content']}")
                print("Falling back to standard processing...")
                agent_result = None
        
        # Prepare state with agent result if available
        state = {
            "data_request": query,
            "consumer_wallet": self.consumer_wallet,
            "provider_wallet": self.provider_wallet,
            "metrics": metrics
        }
        
        # If agent provided a result, include it in the state
        if agent_result:
            state["agent_result"] = agent_result
        
        # Process through workflow (handles payment and delivery)
        result = self.workflow.execute(state)
        
        if "error" in result:
            self.output.print_error(result["error"])
            return None
        else:
            print("\n✅ Response received successfully!")
            self.output.print_transaction_details(
                result['tx_hash'], 
                result['calculated_cost'], 
                result['token_usage']
            )
            
            # Show which agent was used if applicable
            if agent_result:
                print(f"Response generated by agent: {self.agent_name}")
                
            self.output.print_response_content(
                result['data']['content'] if 'data' in result else agent_result['content']
            )
            return result
    
    def show_report(self, export=False):
        """Show the monitoring dashboard report"""
        report = MonitoringDashboard.generate_report()
        self.output.print_report(report)
        self.output.print_transactions(MonitoringDashboard.transactions)
        
        if export:
            self.output.export_report(report, MonitoringDashboard.transactions)