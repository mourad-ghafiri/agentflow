# Agent Framework API Reference

Welcome to the Agent Framework API reference documentation. This documentation provides detailed information about the classes, functions, and interfaces available in the Agent Framework framework.

## Core Components

The Agent Framework framework is organized into several core components:

- [Core](core.md): Base interfaces and application interface
- [Agents](agents.md): Agent implementations and related utilities
- [Tools](tools.md): Tool implementations and related utilities
- [Memory](memory.md): Memory implementations and related utilities
- [Providers](providers.md): LLM provider implementations
- [Orchestration](orchestration.md): Orchestration implementations and related utilities
- [Utilities](utils.md): Miscellaneous utilities

## Getting Started

To get started with the Agent Framework framework, you typically create an application instance and then register providers, tools, and agents:

```python
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider, AnthropicProvider
from framework.tools.web import WebSearchTool
from framework.tools.file import FileReadTool, FileWriteTool

# Create an application
app = AgentFlowApp(name="My Agent App", description="An example agent application")

# Register providers
app.register_provider("openai", OpenAIProvider(api_key="your-openai-api-key"))
app.register_provider("anthropic", AnthropicProvider(api_key="your-anthropic-api-key"))

# Register tools
app.register_tool(WebSearchTool())
app.register_tool(FileReadTool())
app.register_tool(FileWriteTool())

# Create an agent
agent = app.create_agent(
    agent_type="conversational",
    name="My Agent",
    description="A helpful assistant",
    system_prompt="You are a helpful assistant.",
    model="gpt-4",
    provider="openai"
)

# Run the agent
async def main():
    response = await app.run_agent(agent.config.id, "Hello, how are you?")
    print(response.get('content'))

import asyncio
asyncio.run(main())
```

## Advanced Usage

For more advanced usage, you can create orchestrators to coordinate multiple agents:

```python
# Create multiple agents
agent1 = app.create_agent(
    agent_type="react",
    name="Research Agent",
    description="An agent that researches information",
    system_prompt="You are a research assistant.",
    model="gpt-4",
    provider="openai",
    tools=["web_search", "filesystem"]
)

agent2 = app.create_agent(
    agent_type="conversational",
    name="Writing Agent",
    description="An agent that writes content",
    system_prompt="You are a writing assistant.",
    model="gpt-4",
    provider="openai"
)

# Create an orchestrator
orchestrator = await app.create_orchestrator(
    orchestrator_type="sequential",
    name="Research and Write",
    description="Research information and then write content",
    agents=[agent1.config.id, agent2.config.id]
)

# Run the orchestrator
async def main():
    response = await app.run_orchestrator(orchestrator.config.id, "Write a summary of quantum computing")
    print(response)

import asyncio
asyncio.run(main())
```

## Extending the Framework

The Agent Framework framework is designed to be extensible. You can create custom agents, tools, memory systems, and orchestrators by implementing the appropriate interfaces.

For example, to create a custom tool:

```python
from framework.tools.base import Tool, ToolSpec

class MyCustomTool(Tool):
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="my_custom_tool",
            description="A custom tool that does something useful",
            parameters={
                "param1": {
                    "type": "string",
                    "description": "The first parameter"
                },
                "param2": {
                    "type": "integer",
                    "description": "The second parameter"
                }
            },
            required_parameters=["param1"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        # Implement the tool's functionality
        param1 = parameters.get("param1")
        param2 = parameters.get("param2", 0)
        
        # Do something with the parameters
        result = f"Processed {param1} with {param2}"
        
        return result

# Register the custom tool
app.register_tool(MyCustomTool())
```

## API Reference

For detailed information about specific components, refer to the following sections:

- [Core API](core.md)
- [Agents API](agents.md)
- [Tools API](tools.md)
- [Memory API](memory.md)
- [Providers API](providers.md)
- [Orchestration API](orchestration.md)
- [Utilities API](utils.md) 