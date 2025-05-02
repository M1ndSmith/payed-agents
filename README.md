# Payed Agents

A CLI application that implements a pay-per-query system using the CDP (Coinbase Developer Docs) to facilitate transactions between consumers and providers in AI agent workflows.

## Overview

This application enables secure and transparent payment processing for AI agent interactions, where consumers can submit queries and pay for responses from AI providers. The system uses blockchain-based transactions via CDP to handle payments.

## Features

- Pay-per-query system for AI agent interactions
- Secure wallet management for both consumers and providers
- LLM integration using LangChain and Groq
- Workflow management with LangGraph
- Performance metrics and transaction monitoring
- CLI interface for easy interaction

## Prerequisites

Before using this application, you need:

1. **Pre-filled wallets with ETH and USDC**
   - Both consumer and provider wallets must have ETH for gas fees
   - Consumer wallet must have sufficient USDC for payments
   - You can use testnet faucets to get test ETH and USDC

2. **API Keys**
   - Create and add your CDP API key to `api-key/cdp_api_key.json`
   - ArXiv tool requires no API key (used by paper_researcher agent)
   - For Google Search, set environment variables `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` (optional)

## Configuration

1. The application uses a YAML configuration file (`config.yaml`) to manage settings
2. Key configuration includes:
   - LLM providers and models
   - Wallet settings
   - File paths
   - Agent definitions

You can modify the `config.yaml` file to adjust these settings.

## Usage

Process a query with default settings:
```
python main.py --query "Your query text here"
```

Process a query from a file:
```
python main.py --file path/to/query.txt
```

Generate a report:
```
python main.py --query "Your query" --export-report
```

Specify a different LLM provider:
```
python main.py --query "Your query" --provider anthropic
```

Specify both provider and model:
```
python main.py --query "Your query" --provider openai --model gpt-4o-mini
```

Use a specific agent for processing:
```
python main.py --query "What are the latest papers on LLMs?" --agent paper_researcher
```

List available agents:
```
python main.py --list-agents
```

List available models for a provider:
```
python main.py --list-models --provider anthropic
```

Use a custom configuration file:
```
python main.py --query "Your query" --config my_custom_config.yaml
```

## Available LLM Providers

The default configuration includes the following providers and models:

- **groq** (default)
  - llama3-8b-8192 (default)
  - llama3-70b-8192
  - mixtral-8x7b-32768

- **anthropic**
  - claude-3-5-sonnet-20240620 (default)
  - claude-3-opus-20240229
  - claude-3-haiku-20240307

- **openai**
  - gpt-4o (default)
  - gpt-4o-mini
  - gpt-3.5-turbo

## Available Agents

The system includes specialized agents for different tasks:

- **basic_llm** (default): Simple LLM-based agent without tools
- **paper_researcher**: Scientific paper research agent using arXiv (fully functional for demonstration)
- **web_researcher**: Web search agent with Google Search (demo purposes only, requires API keys)
- **code_assistant**: Programming assistant with access to documentation (demo purposes only)

> **Note:** Currently, only the `paper_researcher` agent is fully functional for demonstration purposes without additional configuration. The other specialized agents are included as examples and would require additional API keys and configuration to work properly.

## Custom Agents

You can define custom agents in the `config.yaml` file:

```yaml
agents:
  definitions:
    my_custom_agent:
      description: "Custom agent description"
      type: "tool_augmented"
      provider: "groq"
      model: "llama3-70b-8192"
      temperature: 0.5
      prompt_template: "You are a custom assistant that helps with {request}."
      tools:
        - "tool_name"
```

## Dependencies

- cdp-sdk: Handles blockchain transactions
- langchain: Framework for LLM applications
- langgraph: Workflow orchestration
- langchain-groq: Groq LLM integration
- pandas: Data analysis tools
- pyyaml: YAML file processing
- langchain-openai, langchain-anthropic: Additional LLM provider integrations



