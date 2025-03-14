# Agents API Reference

This document provides detailed API reference for the agent components of the Agent Framework framework.

## Base Agent Interface

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

### `AgentState`

State of an agent.

```python
class AgentState(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    current_iteration: int = 0
    last_tool_call: Optional[Dict[str, Any]] = None
    last_tool_result: Optional[Any] = None
    status: str = "idle"  # idle, running, completed, failed
    error: Optional[str] = None
```

### `Message`

Message in a conversation.

```python
class Message(BaseModel):
    role: str  # system, user, assistant, tool
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
```

## Agent Implementations

### `ConversationalAgent`

Basic conversational agent.

```python
class ConversationalAgent(Agent):
    def __init__(self, 
                name: str, 
                description: str, 
                system_prompt: str,
                model: str,
                provider: str,
                memory_type: str = "conversation",
                memory_config: Optional[Dict[str, Any]] = None,
                max_iterations: int = 10,
                temperature: float = 0.7):
        """
        Initialize the conversational agent.
        
        Args:
            name: Name of the agent.
            description: Description of the agent.
            system_prompt: System prompt for the agent.
            model: Model to use.
            provider: Provider to use.
            memory_type: Type of memory to use.
            memory_config: Configuration for the memory.
            max_iterations: Maximum number of iterations.
            temperature: Sampling temperature.
        """
        
    @property
    def config(self) -> AgentConfig:
        """Return the agent's configuration."""
        
    @property
    def state(self) -> AgentState:
        """Return the current state of the agent."""
        
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Message:
        """
        Run the agent on an input.
        
        Args:
            input_message: Input message or string.
            tools: Optional list of tools to make available to the agent.
            
        Returns:
            The agent's response message.
        """
        
    async def reset(self) -> None:
        """Reset the agent to its initial state."""
```

### `ReActAgent`

Agent that implements the ReAct (Reasoning and Acting) pattern.

```python
class ReActAgent(Agent):
    def __init__(self, 
                name: str, 
                description: str, 
                system_prompt: str,
                model: str,
                provider: str,
                tools: Optional[List[str]] = None,
                memory_type: str = "conversation",
                memory_config: Optional[Dict[str, Any]] = None,
                max_iterations: int = 10,
                temperature: float = 0.7):
        """
        Initialize the ReAct agent.
        
        Args:
            name: Name of the agent.
            description: Description of the agent.
            system_prompt: System prompt for the agent.
            model: Model to use.
            provider: Provider to use.
            tools: List of tool IDs to make available to the agent.
            memory_type: Type of memory to use.
            memory_config: Configuration for the memory.
            max_iterations: Maximum number of iterations.
            temperature: Sampling temperature.
        """
        
    @property
    def config(self) -> AgentConfig:
        """Return the agent's configuration."""
        
    @property
    def state(self) -> AgentState:
        """Return the current state of the agent."""
        
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Any:
        """
        Run the agent on an input.
        
        Args:
            input_message: Input message or string.
            tools: Optional list of tools to make available to the agent.
            
        Returns:
            The agent's final response after tool usage.
        """
        
    async def reset(self) -> None:
        """Reset the agent to its initial state."""
```

### `FunctionCallingAgent`

Agent that uses function calling capabilities of LLMs.

```python
class FunctionCallingAgent(Agent):
    def __init__(self, 
                name: str, 
                description: str, 
                system_prompt: str,
                model: str,
                provider: str,
                tools: Optional[List[str]] = None,
                memory_type: str = "conversation",
                memory_config: Optional[Dict[str, Any]] = None,
                max_iterations: int = 10,
                temperature: float = 0.7):
        """
        Initialize the function calling agent.
        
        Args:
            name: Name of the agent.
            description: Description of the agent.
            system_prompt: System prompt for the agent.
            model: Model to use.
            provider: Provider to use.
            tools: List of tool IDs to make available to the agent.
            memory_type: Type of memory to use.
            memory_config: Configuration for the memory.
            max_iterations: Maximum number of iterations.
            temperature: Sampling temperature.
        """
        
    @property
    def config(self) -> AgentConfig:
        """Return the agent's configuration."""
        
    @property
    def state(self) -> AgentState:
        """Return the current state of the agent."""
        
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Any:
        """
        Run the agent on an input.
        
        Args:
            input_message: Input message or string.
            tools: Optional list of tools to make available to the agent.
            
        Returns:
            The agent's final response after tool usage.
        """
        
    async def reset(self) -> None:
        """Reset the agent to its initial state."""
```

### `PlannerAgent`

Agent specialized for planning tasks.

```python
class PlannerAgent(Agent):
    def __init__(self, 
                name: str, 
                description: str, 
                system_prompt: str,
                model: str,
                provider: str,
                memory_type: str = "conversation",
                memory_config: Optional[Dict[str, Any]] = None,
                max_iterations: int = 3,
                temperature: float = 0.7):
        """
        Initialize the planner agent.
        
        Args:
            name: Name of the agent.
            description: Description of the agent.
            system_prompt: System prompt for the agent.
            model: Model to use.
            provider: Provider to use.
            memory_type: Type of memory to use.
            memory_config: Configuration for the memory.
            max_iterations: Maximum number of iterations.
            temperature: Sampling temperature.
        """
        
    @property
    def config(self) -> AgentConfig:
        """Return the agent's configuration."""
        
    @property
    def state(self) -> AgentState:
        """Return the current state of the agent."""
        
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Dict[str, Any]:
        """
        Run the agent on an input to generate a plan.
        
        Args:
            input_message: Input message or string.
            tools: Optional list of tools to make available to the agent.
            
        Returns:
            A plan as a dictionary with steps.
        """
        
    async def reset(self) -> None:
        """Reset the agent to its initial state."""
```

## Agent Factory

### `AgentFactory`

Factory for creating agent instances.

```python
class AgentFactory:
    @staticmethod
    def create(agent_type: str, **kwargs) -> Agent:
        """
        Create an agent instance.
        
        Args:
            agent_type: Type of agent to create.
            **kwargs: Additional arguments to pass to the agent constructor.
            
        Returns:
            The agent instance.
            
        Raises:
            ValueError: If the agent type is not supported.
        """
```

## Utility Functions

```python
def create_agent(agent_type: str, **kwargs) -> Agent:
    """
    Create an agent instance.
    
    Args:
        agent_type: Type of agent to create.
        **kwargs: Additional arguments to pass to the agent constructor.
        
    Returns:
        The agent instance.
    """
    
def get_default_system_prompt(agent_type: str) -> str:
    """
    Get the default system prompt for an agent type.
    
    Args:
        agent_type: Type of agent.
        
    Returns:
        Default system prompt.
    """
    
def format_tool_for_agent(tool: Tool, format_type: str = "openai") -> Dict[str, Any]:
    """
    Format a tool for use with an agent.
    
    Args:
        tool: Tool to format.
        format_type: Format type to use.
        
    Returns:
        Formatted tool specification.
    """
```