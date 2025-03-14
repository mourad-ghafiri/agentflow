# Orchestration API Reference

This document provides detailed API reference for the orchestration components of the Agent Framework framework.

## Base Orchestrator Interface

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

## Orchestrator Implementations

### `SequentialOrchestrator`

Orchestrator that executes agents in a sequential order.

```python
class SequentialOrchestrator(Orchestrator):
    def __init__(self, 
                name: str, 
                description: str, 
                agents: List[str],
                max_steps: int = 50):
        """
        Initialize the sequential orchestrator.
        
        Args:
            name: Name of the orchestrator.
            description: Description of the orchestrator.
            agents: List of agent IDs to execute in sequence.
            max_steps: Maximum number of steps to execute.
        """
        
    @property
    def config(self) -> OrchestratorConfig:
        """Return the orchestrator's configuration."""
        
    async def execute(self, input_data: Any) -> Any:
        """
        Execute the agents in sequence.
        
        Args:
            input_data: Input data for the first agent.
            
        Returns:
            Output from the last agent.
        """
        
    async def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the orchestrator.
        
        Args:
            agent: Agent to add.
        """
        
    async def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from the orchestrator.
        
        Args:
            agent_id: ID of the agent to remove.
        """
```

### `DAGOrchestrator`

Orchestrator that executes agents according to a directed acyclic graph.

```python
class DAGOrchestrator(Orchestrator):
    def __init__(self, 
                name: str, 
                description: str, 
                workflow: Dict[str, Any],
                max_steps: int = 50):
        """
        Initialize the DAG orchestrator.
        
        Args:
            name: Name of the orchestrator.
            description: Description of the orchestrator.
            workflow: Workflow definition as a DAG.
            max_steps: Maximum number of steps to execute.
        """
        
    @property
    def config(self) -> OrchestratorConfig:
        """Return the orchestrator's configuration."""
        
    async def execute(self, input_data: Any) -> Any:
        """
        Execute the workflow.
        
        Args:
            input_data: Input data for the workflow.
            
        Returns:
            Output from the workflow.
        """
        
    async def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the orchestrator.
        
        Args:
            agent: Agent to add.
        """
        
    async def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from the orchestrator.
        
        Args:
            agent_id: ID of the agent to remove.
        """
        
    async def add_edge(self, from_agent_id: str, to_agent_id: str, condition: Optional[Callable[[Any], bool]] = None) -> None:
        """
        Add an edge to the workflow.
        
        Args:
            from_agent_id: ID of the source agent.
            to_agent_id: ID of the target agent.
            condition: Optional condition function for the edge.
        """
        
    async def remove_edge(self, from_agent_id: str, to_agent_id: str) -> None:
        """
        Remove an edge from the workflow.
        
        Args:
            from_agent_id: ID of the source agent.
            to_agent_id: ID of the target agent.
        """
```

### `ReActOrchestrator`

Orchestrator that implements the ReAct (Reasoning and Acting) pattern.

```python
class ReActOrchestrator(Orchestrator):
    def __init__(self, 
                name: str, 
                description: str, 
                agent_id: str,
                tools: List[str],
                max_steps: int = 10):
        """
        Initialize the ReAct orchestrator.
        
        Args:
            name: Name of the orchestrator.
            description: Description of the orchestrator.
            agent_id: ID of the agent to use.
            tools: List of tool IDs to make available to the agent.
            max_steps: Maximum number of steps to execute.
        """
        
    @property
    def config(self) -> OrchestratorConfig:
        """Return the orchestrator's configuration."""
        
    async def execute(self, input_data: Any) -> Any:
        """
        Execute the ReAct loop.
        
        Args:
            input_data: Input data for the agent.
            
        Returns:
            Final output from the agent.
        """
        
    async def add_agent(self, agent: Agent) -> None:
        """
        Set the agent for the orchestrator.
        
        Args:
            agent: Agent to use.
        """
        
    async def remove_agent(self, agent_id: str) -> None:
        """
        Remove the agent from the orchestrator.
        
        Args:
            agent_id: ID of the agent to remove.
        """
        
    async def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the orchestrator.
        
        Args:
            tool: Tool to add.
        """
        
    async def remove_tool(self, tool_id: str) -> None:
        """
        Remove a tool from the orchestrator.
        
        Args:
            tool_id: ID of the tool to remove.
        """
```

### `PlanAndExecuteOrchestrator`

Orchestrator that implements the Plan-and-Execute pattern.

```python
class PlanAndExecuteOrchestrator(Orchestrator):
    def __init__(self, 
                name: str, 
                description: str, 
                planner_agent_id: str,
                executor_agent_id: str,
                tools: List[str],
                max_steps: int = 10):
        """
        Initialize the Plan-and-Execute orchestrator.
        
        Args:
            name: Name of the orchestrator.
            description: Description of the orchestrator.
            planner_agent_id: ID of the agent to use for planning.
            executor_agent_id: ID of the agent to use for execution.
            tools: List of tool IDs to make available to the executor agent.
            max_steps: Maximum number of steps to execute.
        """
        
    @property
    def config(self) -> OrchestratorConfig:
        """Return the orchestrator's configuration."""
        
    async def execute(self, input_data: Any) -> Any:
        """
        Execute the Plan-and-Execute loop.
        
        Args:
            input_data: Input data for the planner agent.
            
        Returns:
            Final output from the executor agent.
        """
        
    async def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the orchestrator.
        
        Args:
            agent: Agent to add.
        """
        
    async def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from the orchestrator.
        
        Args:
            agent_id: ID of the agent to remove.
        """
        
    async def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the orchestrator.
        
        Args:
            tool: Tool to add.
        """
        
    async def remove_tool(self, tool_id: str) -> None:
        """
        Remove a tool from the orchestrator.
        
        Args:
            tool_id: ID of the tool to remove.
        """
```

## Workflow Definition

### `WorkflowStep`

Definition of a step in a workflow.

```python
class WorkflowStep(BaseModel):
    id: str
    agent_id: str
    input_mapping: Dict[str, str] = Field(default_factory=dict)
    output_mapping: Dict[str, str] = Field(default_factory=dict)
    condition: Optional[str] = None
```

### `Workflow`

Definition of a workflow.

```python
class Workflow(BaseModel):
    steps: List[WorkflowStep]
    edges: List[Tuple[str, str]] = Field(default_factory=list)
    initial_step_id: str
    final_step_id: Optional[str] = None
```

## Orchestrator Factory

### `OrchestratorFactory`

Factory for creating orchestrator instances.

```python
class OrchestratorFactory:
    @staticmethod
    def create(orchestrator_type: str, **kwargs) -> Orchestrator:
        """
        Create an orchestrator instance.
        
        Args:
            orchestrator_type: Type of orchestrator to create.
            **kwargs: Additional arguments to pass to the orchestrator constructor.
            
        Returns:
            The orchestrator instance.
            
        Raises:
            ValueError: If the orchestrator type is not supported.
        """
```

## Utility Functions

```python
def create_orchestrator(orchestrator_type: str, **kwargs) -> Orchestrator:
    """
    Create an orchestrator instance.
    
    Args:
        orchestrator_type: Type of orchestrator to create.
        **kwargs: Additional arguments to pass to the orchestrator constructor.
        
    Returns:
        The orchestrator instance.
    """
    
def create_sequential_workflow(agent_ids: List[str]) -> Workflow:
    """
    Create a sequential workflow.
    
    Args:
        agent_ids: List of agent IDs to execute in sequence.
        
    Returns:
        The workflow definition.
    """
    
def create_dag_workflow(steps: List[WorkflowStep], edges: List[Tuple[str, str]]) -> Workflow:
    """
    Create a DAG workflow.
    
    Args:
        steps: List of workflow steps.
        edges: List of edges between steps.
        
    Returns:
        The workflow definition.
    """
``` 