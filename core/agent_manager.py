import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import load_tools
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from config.yaml_config import ConfigLoader


class AgentManager:
    """Manages creation and execution of different agent types"""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize with config file path"""
        self.config_path = config_path
        self.config = ConfigLoader.load_config(config_path)
        self.agents_config = self.config.get('agents', {})
        self.available_tools = self._get_available_tools()
    
    def _get_available_tools(self):
        """Get list of tools that are available in the environment"""
        # Check for tool dependencies and return available tools
        available_tools = ["arxiv"]  # ArXiv is included in langchain by default
        
        # Add Google Search if API key is available
        if os.environ.get('GOOGLE_API_KEY') and os.environ.get('GOOGLE_CSE_ID'):
            available_tools.append("google_search")
        
        # Add Python REPL (always available)
        available_tools.append("python_repl")
        
        # Add Terminal (always available)
        available_tools.append("terminal")
        
        return available_tools
    
    def get_agent_names(self):
        """Get names of all configured agents"""
        return list(self.agents_config.get('definitions', {}).keys())
    
    def get_default_agent(self):
        """Get the default agent name"""
        return self.agents_config.get('default', 'basic_llm')
    
    def get_agent_description(self, agent_name):
        """Get description of a specific agent"""
        agent_config = self.agents_config.get('definitions', {}).get(agent_name, {})
        return agent_config.get('description', f"Agent: {agent_name}")
    
    def _create_llm_for_agent(self, agent_config):
        """Create LLM based on agent configuration"""
        provider = agent_config.get('provider', 'groq')
        model = agent_config.get('model', 'llama3-8b-8192')
        temperature = agent_config.get('temperature', 0.7)
        
        if provider == 'groq':
            return ChatGroq(model=model, temperature=temperature)
        elif provider == 'anthropic':
            return ChatAnthropic(model=model, temperature=temperature)
        elif provider == 'openai':
            return ChatOpenAI(model=model, temperature=temperature)
        else:
            # Default to Groq if provider not recognized
            return ChatGroq(model='llama3-8b-8192', temperature=temperature)
    
    def _load_agent_tools(self, tool_names):
        """Load tools for an agent, filtering to those available"""
        # Filter to tools that are both requested and available
        valid_tools = [tool for tool in tool_names if tool in self.available_tools]
        
        if not valid_tools:
            print("Warning: No valid tools available for this agent")
            return []
        
        try:
            return load_tools(valid_tools)
        except Exception as e:
            print(f"Error loading tools: {str(e)}")
            return []
    
    def create_agent(self, agent_name=None):
        """Create an agent based on configuration"""
        # Get the agent name, defaulting if none provided
        if agent_name is None:
            agent_name = self.get_default_agent()
        
        # Get agent configuration
        agent_config = self.agents_config.get('definitions', {}).get(agent_name, {})
        if not agent_config:
            print(f"Agent '{agent_name}' not found in configuration, using default")
            agent_name = self.get_default_agent()
            agent_config = self.agents_config.get('definitions', {}).get(agent_name, {})
        
        # Create LLM based on agent configuration
        llm = self._create_llm_for_agent(agent_config)
        
        # Determine agent type
        agent_type = agent_config.get('type', 'basic')
        
        if agent_type == 'basic':
            # Simple LLM agent without tools
            agent = llm | StrOutputParser()
            return {
                'name': agent_name,
                'agent': agent,
                'type': 'basic'
            }
        
        elif agent_type == 'tool_augmented':
            # Agent with tools
            tool_names = agent_config.get('tools', [])
            tools = self._load_agent_tools(tool_names)
            
            # Get prompt template
            prompt_template = agent_config.get(
                'prompt_template', 
                "You are a helpful assistant. Answer the following request: {request}"
            )
            
            # Create prompt
            prompt = PromptTemplate(
                input_variables=["request"],
                template=prompt_template
            )
            
            # Create agent
            agent = prompt | llm | StrOutputParser()
            
            return {
                'name': agent_name,
                'agent': agent,
                'tools': tools,
                'type': 'tool_augmented'
            }
        
        else:
            # If agent type not recognized, default to basic
            print(f"Agent type '{agent_type}' not recognized, defaulting to basic")
            agent = llm | StrOutputParser()
            return {
                'name': agent_name,
                'agent': agent,
                'type': 'basic'
            }
    
    def execute_agent(self, agent_name, query):
        """Execute an agent with the provided query"""
        agent_data = self.create_agent(agent_name)
        agent = agent_data['agent']
        
        try:
            result = agent.invoke({"request": query})
            return {
                'content': result,
                'agent': agent_data['name'],
                'success': True
            }
        except Exception as e:
            error_message = f"Error executing agent: {str(e)}"
            print(error_message)
            return {
                'content': error_message,
                'agent': agent_data['name'],
                'success': False
            } 