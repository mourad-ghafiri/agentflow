"""
AgentFlow: Large Language Model Agent Flow

A flexible and powerful framework for building, deploying, and orchestrating LLM-based agents.
"""

__version__ = "0.1.0"

# Core components
from .core.app import AgentFlowApp
from .core.base import (
    Agent, AgentConfig,
    Tool, ToolSpec,
    Orchestrator, OrchestratorConfig,
    Message, AgentState
)

# Providers
from .core.providers import (
    OpenAIProvider,
    AnthropicProvider,
    ProviderRegistry
)

# Tools
from .tools.base import (
    BaseTool,
    FunctionTool,
    PydanticTool,
    ToolRegistry
)

# Agents
from .agents.base import (
    BaseAgent,
    ReActAgent,
    ConversationalAgent,
    FunctionCallingAgent,
    PlannerAgent,
    AgentFactory
)

# Memory
from .memory.base import (
    SimpleMemory,
    MessageMemory,
    MemoryFactory
)

# Orchestration
from .orchestration.base import (
    SequentialOrchestrator,
    DAGOrchestrator,
    OrchestratorFactory
)

# Convenience functions
def create_app(name: str, description: str = "") -> AgentFlowApp:
    """Create a new AgentFlow application."""
    return AgentFlowApp(name=name, description=description)
