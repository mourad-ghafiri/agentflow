"""
Main application interface for the AgentFlow framework.
"""
import json
import os
import asyncio
from typing import Any, Dict, List, Optional, Union, Callable

from .base import Agent, AgentConfig, Orchestrator, OrchestratorConfig, Tool, Message
from ..agents.base import AgentFactory
from ..orchestration.base import OrchestratorFactory
from ..tools.base import ToolRegistry
from ..core.providers import ProviderRegistry

class AgentFlowApp:
    """Main application interface for the AgentFlow framework."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize the application."""
        self.name = name
        self.description = description
        self.agents: Dict[str, Agent] = {}
        self.orchestrators: Dict[str, Orchestrator] = {}
    
    def register_provider(self, name: str, provider: Any) -> None:
        """Register a provider with the framework."""
        ProviderRegistry.register(name, provider)
    
    def register_tool(self, tool: Tool) -> None:
        """Register a tool with the framework."""
        ToolRegistry.register(tool)
    
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
        config = AgentConfig(
            name=name,
            description=description,
            system_prompt=system_prompt,
            model=model,
            provider=provider,
            tools=tools or [],
            **kwargs
        )
        
        agent = AgentFactory.create_agent(agent_type, config)
        self.agents[config.id] = agent
        return agent
    
    async def create_orchestrator(self,
                           orchestrator_type: str,
                           name: str,
                           description: str,
                           agents: List[str],
                           workflow: Dict[str, Any],
                           **kwargs) -> Orchestrator:
        """Create and register an orchestrator.
        
        This is now an async method so we can properly await the add_agent coroutine.
        """
        config = OrchestratorConfig(
            name=name,
            description=description,
            agents=agents,
            workflow=workflow,
            **kwargs
        )
        
        orchestrator = OrchestratorFactory.create_orchestrator(orchestrator_type, config)
        self.orchestrators[config.id] = orchestrator
        
        # Add agents to orchestrator (properly awaited now)
        for agent_id in agents:
            if agent_id in self.agents:
                await orchestrator.add_agent(self.agents[agent_id])
        
        return orchestrator
    
    async def run_agent(self, agent_id: str, input_data: Any) -> Any:
        """Run an agent with the given input data."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        return await agent.run(input_data)
    
    async def run_orchestrator(self, orchestrator_id: str, input_data: Any) -> Any:
        """Run an orchestrator with the given input data."""
        if orchestrator_id not in self.orchestrators:
            raise ValueError(f"Orchestrator {orchestrator_id} not found")
        
        orchestrator = self.orchestrators[orchestrator_id]
        return await orchestrator.execute(input_data)
    
    def save_config(self, filename: str) -> None:
        """Save the application configuration to a file."""
        config = {
            "name": self.name,
            "description": self.description,
            "agents": {
                agent_id: agent.config.dict() 
                for agent_id, agent in self.agents.items()
            },
            "orchestrators": {
                orch_id: orch.config.dict()
                for orch_id, orch in self.orchestrators.items()
            }
        }
        
        with open(filename, "w") as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def load_config(cls, filename: str) -> "AgentFlowApp":
        """Load an application configuration from a file."""
        with open(filename, "r") as f:
            config = json.load(f)
        
        app = cls(config["name"], config.get("description", ""))
        
        # Create agents
        for agent_id, agent_config in config.get("agents", {}).items():
            agent_type = agent_config.pop("type", "react")
            agent = app.create_agent(agent_type, **agent_config)
        
        # Create orchestrators
        for orch_id, orch_config in config.get("orchestrators", {}).items():
            orch_type = orch_config.pop("type", "sequential")
            orchestrator = app.create_orchestrator(orch_type, **orch_config)
        
        return app 