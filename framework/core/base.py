"""
Core base interfaces for the AgentFlow framework.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from pydantic import BaseModel, Field
import uuid

# Type definitions
T = TypeVar('T')
ToolResult = TypeVar('ToolResult')
AgentState = Dict[str, Any]
Message = Dict[str, Any]

class ToolSpec(BaseModel):
    """Specification for a tool that an agent can use."""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    required_parameters: List[str] = Field(default_factory=list)
    return_type: Optional[str] = None

class Tool(ABC):
    """Abstract base class for tools used by agents."""
    
    @property
    @abstractmethod
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        pass
    
    @abstractmethod
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the tool with the given parameters."""
        pass

class MemoryInterface(ABC, Generic[T]):
    """Interface for memory systems used by agents."""
    
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

class LLMProvider(ABC):
    """Abstract interface for LLM providers (OpenAI, Anthropic, etc.)."""
    
    @abstractmethod
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      **kwargs) -> Message:
        """Generate a completion from the LLM."""
        pass

class AgentConfig(BaseModel):
    """Configuration for an agent."""
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

class Agent(ABC):
    """Abstract base class for agents."""
    
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

class OrchestratorConfig(BaseModel):
    """Configuration for an orchestrator."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    agents: List[str]
    workflow: Dict[str, Any]
    max_steps: int = 50

class Orchestrator(ABC):
    """Abstract base class for agent orchestrators."""
    
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