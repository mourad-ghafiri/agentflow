# Getting Started with Agent Framework

Agent Framework (Large Language Model Agent Flow) is a framework for building agent-based applications with large language models (LLMs) in a standardized way. This guide will help you get started with the framework.

## Installation


Or from the source:

```bash
git clone https://github.com/mourad-ghafiri/agentflow.git
cd agentflow
pip install -e .
```

## Basic Usage

Here's a simple example of how to create and run an agent with Agent Framework:

```python
import os
import asyncio
from dotenv import load_dotenv
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider
from framework.tools.base import FunctionTool

# Load environment variables
load_dotenv()

# Define a simple tool
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

async def main():
    # Create the application
    app = AgentFlowApp(name="Hello World App")
    
    # Register OpenAI provider
    openai_api_key = os.getenv("OPENAI_API_KEY")
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Register the greeting tool
    app.register_tool(FunctionTool(greet))
    
    # Create a simple agent
    agent = app.create_agent(
        agent_type="react",
        name="GreetingAgent",
        description="An agent that greets users",
        system_prompt="You are a friendly assistant that greets users. Use the greet tool when a user introduces themselves.",
        model="gpt-3.5-turbo",
        provider="openai",
        tools=["greet"]
    )
    
    # Run the agent
    response = await app.run_agent(agent.config.id, "My name is Alice")
    print(response.get('content'))

if __name__ == "__main__":
    asyncio.run(main())
```

## Creating Tools

Agent Framework provides several ways to create tools:

### Function Tools

The simplest way to create a tool is to wrap a Python function:

```python
from framework.tools.base import FunctionTool

def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers."""
    return a + b

tool = FunctionTool(calculate_sum)
```

### Pydantic Tools

For more complex tools with input validation, use Pydantic models:

```python
from pydantic import BaseModel, Field
from framework.tools.base import PydanticTool
from typing import List

class SearchInput(BaseModel):
    query: str = Field(..., description="The search query")
    max_results: int = Field(5, description="Maximum number of results to return")

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

class SearchResults(BaseModel):
    results: List[SearchResult]

class SearchTool(PydanticTool):
    def __init__(self):
        super().__init__(
            name="search",
            description="Search the web for information",
            input_model=SearchInput,
            output_model=SearchResults
        )
    
    async def _execute_with_validated_input(self, validated_input: SearchInput) -> SearchResults:
        # Actual implementation would call a search API
        results = [
            SearchResult(
                title=f"Result for {validated_input.query}",
                url=f"https://example.com/search?q={validated_input.query}",
                snippet=f"This is a snippet about {validated_input.query}"
            )
            for _ in range(validated_input.max_results)
        ]
        return SearchResults(results=results)
```

## Creating Agents

Agent Framework currently supports the ReAct agent pattern, which combines reasoning and acting:

```python
agent = app.create_agent(
    agent_type="react",
    name="ResearchAgent",
    description="An agent that researches topics",
    system_prompt="You are a research assistant. When given a topic, use the search tool to find information about it.",
    model="gpt-4",
    provider="openai",
    tools=["search"]
)
```

## Orchestrating Multiple Agents

Agent Framework supports two types of orchestration: sequential and DAG-based.

### Sequential Orchestration

Sequential orchestration runs agents in a linear sequence:

```python
orchestrator = app.create_orchestrator(
    orchestrator_type="sequential",
    name="SimpleWorkflow",
    description="A simple sequential workflow",
    agents=[agent1.config.id, agent2.config.id, agent3.config.id],
    workflow={
        "sequence": [
            agent1.config.id,
            agent2.config.id, 
            agent3.config.id
        ]
    }
)

result = await app.run_orchestrator(orchestrator.config.id, "Initial input")
```

### DAG-based Orchestration

DAG-based orchestration allows for more complex workflows with dependencies:

```python
orchestrator = app.create_orchestrator(
    orchestrator_type="dag",
    name="ComplexWorkflow",
    description="A complex DAG workflow",
    agents=[agent1.config.id, agent2.config.id, agent3.config.id, agent4.config.id],
    workflow={
        "entry_point": agent1.config.id,
        "final_node": agent4.config.id,
        "dag": {
            agent1.config.id: {
                "dependencies": [],
                "description": "Start of the workflow"
            },
            agent2.config.id: {
                "dependencies": [agent1.config.id],
                "description": "Second step in one branch"
            },
            agent3.config.id: {
                "dependencies": [agent1.config.id],
                "description": "Second step in another branch"
            },
            agent4.config.id: {
                "dependencies": [agent2.config.id, agent3.config.id],
                "description": "Final step that combines results"
            }
        }
    }
)
```

## Next Steps

Check out the examples directory for more advanced examples of using Agent Framework, including:

- Single-agent applications
- Multi-agent workflows
- Custom tool creation
- DAG-based orchestration

For complete API reference, see the API documentation.

## Contributing

Contributions to Agent Framework are welcome! Please see the CONTRIBUTING.md file for guidelines. 