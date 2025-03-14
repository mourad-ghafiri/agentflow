"""
Base agent implementations for the AgentFlow framework.
"""
import json
import uuid
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from ..core.base import Agent, AgentConfig, AgentState, Message, Tool, ToolSpec
from ..core.providers import LLMProvider, ProviderRegistry
from ..memory.base import MemoryFactory, MessageMemory
from ..tools.base import ToolRegistry

class BaseAgent(Agent):
    """Base implementation of the Agent interface."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the agent with its configuration."""
        self._config = config
        self._state: AgentState = {"messages": [], "iterations": 0}
        self._memory = MemoryFactory.create_memory("message")
        
        # Add system message to memory
        # Initialize as empty first, system message will be added when run is called
        # Do not call async method in init
    
    async def _add_system_message(self):
        """Add the system message to memory."""
        system_message = {
            "role": "system",
            "content": self._config.system_prompt
        }
        await self._memory.add(system_message)
    
    @property
    def config(self) -> AgentConfig:
        """Return the agent's configuration."""
        return self._config
    
    @property
    def state(self) -> AgentState:
        """Return the current state of the agent."""
        return self._state.copy()
    
    async def reset(self) -> None:
        """Reset the agent to its initial state."""
        await self._memory.clear()
        self._state = {"messages": [], "iterations": 0}
        await self._add_system_message()
    
    async def _run_iteration(self, 
                           messages: List[Message], 
                           tools: Optional[List[Tool]] = None) -> Message:
        """Run a single iteration of the agent's decision loop."""
        raise NotImplementedError("Subclasses must implement _run_iteration")
    
    async def _get_provider(self) -> LLMProvider:
        """Get the LLM provider for this agent."""
        return ProviderRegistry.get(self._config.provider)
    
    async def _get_tools(self, tool_names: Optional[List[str]] = None) -> List[Tool]:
        """Get the tools available to this agent."""
        if tool_names is None:
            tool_names = self._config.tools
        
        tools = []
        for name in tool_names:
            try:
                tools.append(ToolRegistry.get(name))
            except ValueError:
                # Tool not found, skip
                pass
        
        return tools
    
    async def _get_tool_specs(self, tools: List[Tool]) -> List[ToolSpec]:
        """Get the specifications for the given tools."""
        return [tool.spec for tool in tools]
    
    @abstractmethod
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Any:
        """Run the agent on an input with the specified tools."""
        pass

class ConversationalAgent(BaseAgent):
    """A basic conversational agent without tool use capabilities."""
    
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Message:
        """Run the agent to respond to the input message."""
        # Make sure system message is added
        messages = await self._memory.get_conversation_history()
        if not any(msg.get("role") == "system" for msg in messages):
            await self._add_system_message()
        
        # Convert string input to message if needed
        if isinstance(input_message, str):
            input_message = {"role": "user", "content": input_message}
        
        # Add input message to memory
        await self._memory.add(input_message)
        
        # Get conversation history
        messages = await self._memory.get_conversation_history()
        
        # Generate response
        provider = await self._get_provider()
        response = await provider.complete(
            messages=messages,
            model=self._config.model,
            temperature=self._config.temperature
        )
        
        # Add response to memory
        await self._memory.add(response)
        
        # Return response
        return response
    
    async def _run_iteration(self, 
                           messages: List[Message], 
                           tools: Optional[List[Tool]] = None) -> Message:
        """Run a single iteration of the agent's decision loop."""
        provider = await self._get_provider()
        
        # Generate completion
        response = await provider.complete(
            messages=messages,
            model=self._config.model,
            temperature=self._config.temperature
        )
        
        return response

class ReActAgent(BaseAgent):
    """An agent that uses the ReAct (Reasoning and Acting) pattern."""
    
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Any:
        """Run the agent to respond to the input message."""
        # Make sure system message is added
        messages = await self._memory.get_conversation_history()
        if not any(msg.get("role") == "system" for msg in messages):
            await self._add_system_message()
        
        # Convert string input to message if needed
        if isinstance(input_message, str):
            input_message = {"role": "user", "content": input_message}
        
        # Add input message to memory
        await self._memory.add(input_message)
        
        # Get tools
        if tools is None:
            tools = await self._get_tools()
        
        # Get conversation history
        messages = await self._memory.get_conversation_history()
        
        # Run iterations
        iterations = 0
        max_iterations = self._config.max_iterations
        final_response = None
        
        while iterations < max_iterations:
            # Update state
            iterations += 1
            self._state["iterations"] = iterations
            
            # Run iteration
            response = await self._run_iteration(messages, tools)
            
            # Check if tool calls are present
            tool_calls = response.get("tool_calls", [])
            if not tool_calls:
                # No tool calls, this is the final response
                await self._memory.add(response)
                final_response = response
                break
            
            # Process tool calls
            await self._memory.add(response)
            
            for tool_call in tool_calls:
                # Get tool call details
                function = tool_call.get("function", {})
                tool_name = function.get("name")
                arguments_str = function.get("arguments", "{}")
                
                # Find the tool
                tool = next((t for t in tools if t.spec.name == tool_name), None)
                if not tool:
                    # Tool not found, create error response
                    tool_response = {
                        "role": "tool",
                        "tool_call_id": tool_call.get("id"),
                        "content": f"Error: Tool {tool_name} not found"
                    }
                else:
                    # Execute the tool
                    try:
                        arguments = json.loads(arguments_str)
                        result = await tool.execute(arguments)
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool_call.get("id"),
                            "content": str(result)
                        }
                    except Exception as e:
                        # Tool execution failed
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool_call.get("id"),
                            "content": f"Error: {str(e)}"
                        }
                
                # Add tool response to memory
                await self._memory.add(tool_response)
            
            # Update messages for next iteration
            messages = await self._memory.get_conversation_history()
        
        # Return final response
        return final_response
    
    async def _run_iteration(self, 
                           messages: List[Message], 
                           tools: Optional[List[Tool]] = None) -> Message:
        """Run a single iteration of the agent's decision loop."""
        provider = await self._get_provider()
        tool_specs = await self._get_tool_specs(tools) if tools else None
        
        # Generate completion
        response = await provider.complete(
            messages=messages,
            tools=tool_specs,
            model=self._config.model,
            temperature=self._config.temperature
        )
        
        return response

class FunctionCallingAgent(BaseAgent):
    """An agent that uses function calling capabilities of LLMs."""
    
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Any:
        """Run the agent to respond to the input message."""
        # Make sure system message is added
        messages = await self._memory.get_conversation_history()
        if not any(msg.get("role") == "system" for msg in messages):
            await self._add_system_message()
        
        # Convert string input to message if needed
        if isinstance(input_message, str):
            input_message = {"role": "user", "content": input_message}
        
        # Add input message to memory
        await self._memory.add(input_message)
        
        # Get tools
        if tools is None:
            tools = await self._get_tools()
        
        # Get conversation history
        messages = await self._memory.get_conversation_history()
        
        # Run iterations
        iterations = 0
        max_iterations = self._config.max_iterations
        final_response = None
        
        while iterations < max_iterations:
            # Update state
            iterations += 1
            self._state["iterations"] = iterations
            
            # Run iteration
            response = await self._run_iteration(messages, tools)
            
            # Check if function calls are present
            tool_calls = response.get("tool_calls", [])
            if not tool_calls:
                # No tool calls, this is the final response
                await self._memory.add(response)
                final_response = response
                break
            
            # Process tool calls
            await self._memory.add(response)
            
            for tool_call in tool_calls:
                # Get tool call details
                function = tool_call.get("function", {})
                tool_name = function.get("name")
                arguments_str = function.get("arguments", "{}")
                
                # Find the tool
                tool = next((t for t in tools if t.spec.name == tool_name), None)
                if not tool:
                    # Tool not found, create error response
                    tool_response = {
                        "role": "tool",
                        "tool_call_id": tool_call.get("id"),
                        "content": f"Error: Tool {tool_name} not found"
                    }
                else:
                    # Execute the tool
                    try:
                        arguments = json.loads(arguments_str)
                        result = await tool.execute(arguments)
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool_call.get("id"),
                            "content": str(result)
                        }
                    except Exception as e:
                        # Tool execution failed
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool_call.get("id"),
                            "content": f"Error: {str(e)}"
                        }
                
                # Add tool response to memory
                await self._memory.add(tool_response)
            
            # Update messages for next iteration
            messages = await self._memory.get_conversation_history()
        
        # Return final response
        return final_response
    
    async def _run_iteration(self, 
                           messages: List[Message], 
                           tools: Optional[List[Tool]] = None) -> Message:
        """Run a single iteration of the agent's decision loop."""
        provider = await self._get_provider()
        tool_specs = await self._get_tool_specs(tools) if tools else None
        
        # Generate completion with function calling
        response = await provider.complete(
            messages=messages,
            tools=tool_specs,
            model=self._config.model,
            temperature=self._config.temperature
        )
        
        return response

class PlannerAgent(BaseAgent):
    """An agent specialized for planning tasks."""
    
    async def run(self, 
                input_message: Union[str, Message], 
                tools: Optional[List[Tool]] = None) -> Dict[str, Any]:
        """Run the agent to generate a plan."""
        # Make sure system message is added
        messages = await self._memory.get_conversation_history()
        if not any(msg.get("role") == "system" for msg in messages):
            await self._add_system_message()
        
        # Convert string input to message if needed
        if isinstance(input_message, str):
            input_message = {"role": "user", "content": input_message}
        
        # Add input message to memory
        await self._memory.add(input_message)
        
        # Get conversation history
        messages = await self._memory.get_conversation_history()
        
        # Generate plan
        provider = await self._get_provider()
        response = await provider.complete(
            messages=messages,
            model=self._config.model,
            temperature=self._config.temperature
        )
        
        # Add response to memory
        await self._memory.add(response)
        
        # Parse the plan from the response
        try:
            # Try to extract a JSON plan from the response
            content = response.get("content", "")
            # Look for JSON-like content between triple backticks
            import re
            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if json_match:
                plan_json = json_match.group(1)
                plan = json.loads(plan_json)
            else:
                # If no JSON found, return the response as a simple plan
                plan = {
                    "description": "Generated plan",
                    "steps": [{"description": content}]
                }
        except Exception as e:
            # If parsing fails, return a simple plan
            plan = {
                "description": "Generated plan",
                "steps": [{"description": response.get("content", "")}],
                "parsing_error": str(e)
            }
        
        return plan
    
    async def _run_iteration(self, 
                           messages: List[Message], 
                           tools: Optional[List[Tool]] = None) -> Message:
        """Run a single iteration of the agent's decision loop."""
        provider = await self._get_provider()
        
        # Generate completion
        response = await provider.complete(
            messages=messages,
            model=self._config.model,
            temperature=self._config.temperature
        )
        
        return response

class AgentFactory:
    """Factory for creating agent instances."""
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig) -> Agent:
        """Create an agent of the specified type."""
        if agent_type == "react":
            return ReActAgent(config)
        elif agent_type == "conversational":
            return ConversationalAgent(config)
        elif agent_type == "function_calling":
            return FunctionCallingAgent(config)
        elif agent_type == "planner":
            return PlannerAgent(config)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
