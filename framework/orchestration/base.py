"""
Base orchestration implementations for the AgentFlow framework.
"""
import json
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union

from ..core.base import Agent, Orchestrator, OrchestratorConfig, Message, Tool
from ..agents.base import AgentFactory
from ..memory.base import MemoryFactory

class BaseOrchestrator(Orchestrator):
    """Base implementation of the Orchestrator interface."""
    
    def __init__(self, config: OrchestratorConfig):
        """Initialize the orchestrator with its configuration."""
        self._config = config
        self._agents: Dict[str, Agent] = {}
        self._memory = MemoryFactory.create_memory("simple")
    
    @property
    def config(self) -> OrchestratorConfig:
        """Return the orchestrator's configuration."""
        return self._config
    
    async def add_agent(self, agent: Agent) -> None:
        """Add an agent to the orchestrator."""
        self._agents[agent.config.id] = agent
    
    async def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the orchestrator."""
        if agent_id in self._agents:
            del self._agents[agent_id]
    
    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the orchestration workflow with the given input data."""
        pass

    def _format_input(self, input_data: Any) -> Union[str, Dict[str, Any]]:
        """Format input data for an agent.
        
        If input_data is not a message (dict with 'role' and 'content'), 
        convert it to a user message with the content as string.
        """
        if isinstance(input_data, dict) and "role" in input_data and "content" in input_data:
            # Already a properly formatted message
            return input_data
            
        # Convert to a user message
        content = str(input_data) if not isinstance(input_data, str) else input_data
        return {"role": "user", "content": content}

class SequentialOrchestrator(BaseOrchestrator):
    """An orchestrator that executes agents in sequence."""
    
    async def execute(self, input_data: Any) -> Any:
        """Execute agents in sequence and return the final result."""
        # Get the sequence of agent IDs from workflow
        agent_sequence = self._config.workflow.get("sequence", [])
        if not agent_sequence:
            raise ValueError("Workflow must specify a sequence of agent IDs")
        
        # Process input through each agent in sequence
        current_input = self._format_input(input_data)
        
        for agent_id in agent_sequence:
            # Get the agent
            agent = self._agents.get(agent_id)
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Run the agent
            current_input = await agent.run(current_input)
        
        return current_input

class DAGOrchestrator(BaseOrchestrator):
    """An orchestrator that executes agents according to a directed acyclic graph."""
    
    async def execute(self, input_data: Any) -> Any:
        """Execute agents according to a DAG workflow."""
        # Get the DAG structure from workflow
        dag = self._config.workflow.get("dag", {})
        if not dag:
            raise ValueError("Workflow must specify a DAG structure")
        
        # Get the entry point
        entry_point = self._config.workflow.get("entry_point")
        if not entry_point:
            raise ValueError("Workflow must specify an entry point")
        
        # Set initial input
        results = {entry_point: self._format_input(input_data)}
        
        # Process all nodes
        steps = 0
        max_steps = self._config.max_steps
        
        # Set of nodes that have been processed
        processed_nodes = set()
        
        while steps < max_steps and len(processed_nodes) < len(dag):
            steps += 1
            
            # Find nodes that can be processed (all dependencies are in results)
            for node_id, node_config in dag.items():
                # Skip if already processed
                if node_id in processed_nodes:
                    continue
                
                # Check if all dependencies are satisfied
                dependencies = node_config.get("dependencies", [])
                if all(dep in results for dep in dependencies):
                    # Get the agent
                    agent = self._agents.get(node_id)
                    if not agent:
                        raise ValueError(f"Agent {node_id} not found")
                    
                    # Prepare input for the agent
                    agent_input = node_config.get("input_mapping")
                    if agent_input:
                        # Map inputs from dependency results
                        mapped_input = {}
                        for input_key, mapping in agent_input.items():
                            # Check if the mapping has a dot notation (node.attribute)
                            if "." in mapping:
                                source_node, source_key = mapping.split(".", 1)
                                if source_node in results:
                                    source_value = results[source_node]
                                    if isinstance(source_value, dict) and source_key in source_value:
                                        mapped_input[input_key] = source_value[source_key]
                                    else:
                                        # Couldn't extract the specific attribute, use the whole value
                                        mapped_input[input_key] = source_value
                            else:
                                # Simple mapping - just use the result from the specified node
                                source_node = mapping
                                if source_node in results:
                                    mapped_input[input_key] = results[source_node]
                        
                        # Format the input as a user message if it's not already a message
                        formatted_input = self._format_input(mapped_input)
                        
                        # Run the agent with mapped input
                        result = await agent.run(formatted_input)
                    else:
                        # Use the result of the first dependency as input
                        dependency_results = [results[dep] for dep in dependencies]
                        agent_input = dependency_results[0] if dependency_results else input_data
                        
                        # Format the input if needed
                        formatted_input = self._format_input(agent_input)
                        
                        result = await agent.run(formatted_input)
                    
                    # Store the result
                    results[node_id] = result
                    processed_nodes.add(node_id)
        
        # Return the result of the final node
        final_node = self._config.workflow.get("final_node")
        if not final_node:
            raise ValueError("Workflow must specify a final node")
        
        if final_node not in results:
            raise ValueError(f"Final node {final_node} was not processed")
        
        return results[final_node]

class OrchestratorFactory:
    """Factory for creating orchestrator instances."""
    
    @staticmethod
    def create_orchestrator(orchestrator_type: str, config: OrchestratorConfig) -> Orchestrator:
        """Create an orchestrator of the specified type."""
        if orchestrator_type == "sequential":
            return SequentialOrchestrator(config)
        elif orchestrator_type == "dag":
            return DAGOrchestrator(config)
        else:
            raise ValueError(f"Unknown orchestrator type: {orchestrator_type}") 