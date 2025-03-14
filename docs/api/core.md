# Core API Reference

This document provides detailed API reference for the core components of the Agent Framework framework.

## Base Interfaces

### `Tool`

Abstract base class for tools that agents can use.

```python
class Tool(ABC):
    @property
    @abstractmethod
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        pass
    
    @abstractmethod
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the tool with the given parameters."""
        pass
```

### `Agent`

Abstract base class for LLM-based agents.

```python
class Agent(ABC):
    @property
    @abstractmethod
    def config(self) -> AgentConfig:
        """Return the agent's configuration."""
        pass
    
    @property
    @abstractmethod
    def state(self) -> AgentState:
        """Return the current state of the agent."""
        pass
    
    @abstractmethod
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Any:
        """Run the agent on an input with the specified tools."""
        pass
    
    @abstractmethod
    async def reset(self) -> None:
        """Reset the agent to its initial state."""
        pass
```

### `Orchestrator`

Abstract base class for agent orchestrators.

```python
class Orchestrator(ABC):
    @property
    @abstractmethod
    def config(self) -> OrchestratorConfig:
        """Return the orchestrator's configuration."""
        pass
    
    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the orchestration workflow with the given input data."""
        pass
    
    @abstractmethod
    async def add_agent(self, agent: Agent) -> None:
        """Add an agent to the orchestrator."""
        pass
    
    @abstractmethod
    async def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the orchestrator."""
        pass
```

### `LLMProvider`

Abstract interface for LLM providers.

```python
class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      **kwargs) -> Message:
        """Generate a completion from the LLM."""
        pass
```

### `MemoryInterface`

Interface for memory systems used by agents.

```python
class MemoryInterface(ABC, Generic[T]):
    @abstractmethod
    async def add(self, item: T) -> None:
        """Add an item to memory."""
        pass
    
    @abstractmethod
    async def get(self, query: Any, **kwargs) -> List[T]:
        """Retrieve items from memory based on a query."""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all items from memory."""
        pass
```

## Configuration Models

### `ToolSpec`

Specification for a tool that an agent can use.

```python
class ToolSpec(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    required_parameters: List[str] = Field(default_factory=list)
    return_type: Optional[str] = None
```

### `AgentConfig`

Configuration for an agent.

```python
class AgentConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    tools: List[str] = Field(default_factory=list)
    system_prompt: str
    model: str
    provider: str
    memory_config: Dict[str, Any] = Field(default_factory=dict)
    max_iterations: int = 10
    temperature: float = 0.7
```

### `OrchestratorConfig`

Configuration for an orchestrator.

```python
class OrchestratorConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    agents: List[str]
    workflow: Dict[str, Any]
    max_steps: int = 50
```

## Application Interface

### `AgentFlowApp`

Main application interface for the Agent Framework framework.

```python
class AgentFlowApp:
    def __init__(self, name: str, description: str = ""):
        """Initialize the application."""
        
    def register_provider(self, name: str, provider: Any) -> None:
        """Register a provider with the framework."""
        
    def register_tool(self, tool: Tool) -> None:
        """Register a tool with the framework."""
        
    def create_agent(self, 
                    agent_type: str, 
                    name: str, 
                    description: str, 
                    system_prompt: str,
                    model: str,
                    provider: str,
                    tools: Optional[List[str]] = None,
                    **kwargs) -> Agent:
        """Create and register an agent."""
        
    async def create_orchestrator(self,
                           orchestrator_type: str,
                           name: str,
                           description: str,
                           agents: List[str],
                           workflow: Dict[str, Any],
                           **kwargs) -> Orchestrator:
        """Create and register an orchestrator."""
        
    async def run_agent(self, agent_id: str, input_data: Any) -> Any:
        """Run an agent with the given input data."""
        
    async def run_orchestrator(self, orchestrator_id: str, input_data: Any) -> Any:
        """Run an orchestrator with the given input data."""
        
    def save_config(self, filename: str) -> None:
        """Save the application configuration to a file."""
        
    @classmethod
    def load_config(cls, filename: str) -> "AgentFlowApp":
        """Load an application configuration from a file."""
```

### Convenience Functions

```python
def create_app(name: str, description: str = "") -> AgentFlowApp:
    """Create a new Agent Framework application."""
    return AgentFlowApp(name=name, description=description)
``` 