import time
import argparse
import sys
import os
from cli.app import CDPCliApp
from config.paths import Paths
from config.yaml_config import ConfigLoader
from core.llm import LLMProvider
from core.agent_manager import AgentManager

def main():
    # Load config
    config = ConfigLoader.load_config()
    
    # Get available providers, models, and agents
    available_providers = list(config.get('llm', {}).get('models', {}).keys())
    
    # Initialize agent manager
    agent_manager = AgentManager()
    available_agents = agent_manager.get_agent_names()
    default_agent = agent_manager.get_default_agent()
    
    parser = argparse.ArgumentParser(description="CDP CLI Application")
    parser.add_argument("--query", help="Query to process")
    parser.add_argument("--file", help="Path to file containing query")
    parser.add_argument("--export-report", action="store_true", help="Export report to JSON")
    parser.add_argument("--config", help="Path to YAML config file", default="config.yaml")
    
    # LLM options
    llm_group = parser.add_argument_group('LLM Options')
    llm_group.add_argument("--provider", choices=available_providers, help="LLM provider to use")
    llm_group.add_argument("--model", help="Specific model to use with the selected provider")
    llm_group.add_argument("--list-models", action="store_true", help="List available models for the specified provider")
    
    # Agent options
    agent_group = parser.add_argument_group('Agent Options')
    agent_group.add_argument("--agent", choices=available_agents, help="Agent to use for processing query")
    agent_group.add_argument("--list-agents", action="store_true", help="List available agents and their descriptions")
    
    args = parser.parse_args()
    
    # If list-models flag is set, just show available models and exit
    if args.list_models:
        provider = args.provider or ConfigLoader.get_llm_provider()
        models = LLMProvider.list_available_models(provider)
        print(f"Available models for {provider}:")
        for model in models:
            print(f"  - {model}")
        sys.exit(0)
    
    # If list-agents flag is set, show available agents and exit
    if args.list_agents:
        print("Available agents:")
        for agent_name in available_agents:
            description = agent_manager.get_agent_description(agent_name)
            print(f"  - {agent_name}: {description}")
        print(f"\nDefault agent: {default_agent}")
        sys.exit(0)
    
    # Get query from file or command line
    query = None
    if args.query:
        query = args.query
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: Query file does not exist: {args.file}")
            sys.exit(1)
        with open(args.file, 'r') as f:
            query = f.read()
    else:
        print("Error: Either --query or --file must be provided")
        sys.exit(1)
    
    # Get paths from config
    paths = ConfigLoader.get_paths()
    
    # Initialize CLI application with config
    app = CDPCliApp(
        cdp_api_path=paths.get('cdp_api', "api-key/cdp_api_key.json"),
        consumer_seed_path=paths.get('consumer_seed', "wallets/consumer_seed.json"),
        provider_seed_path=paths.get('provider_seed', "wallets/provider_seed.json"),
        llm_provider=args.provider,
        llm_model=args.model,
        agent_name=args.agent,
        config_path=args.config
    )
    if not app.initialize():
        print("Initialization failed. Exiting.")
        sys.exit(1)
    
    # Process query and show report
    app.process_query(query)
    app.show_report(export=args.export_report)

if __name__ == "__main__":
    main()