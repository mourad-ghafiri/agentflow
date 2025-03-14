"""
LLM Provider implementations for different language model providers.
"""
import json
from typing import Any, Dict, List, Optional, Union

import httpx
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from .base import LLMProvider, Message, ToolSpec

class OpenAIProvider(LLMProvider):
    """Provider implementation for OpenAI's API."""
    
    def __init__(self, api_key: str, organization: Optional[str] = None):
        """Initialize the OpenAI provider with API credentials."""
        self.client = AsyncOpenAI(api_key=api_key, organization=organization)
    
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      **kwargs) -> Message:
        """Generate a completion from OpenAI."""
        tools_param = None
        if tools:
            tools_param = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": tool.parameters,
                            "required": tool.required_parameters
                        }
                    }
                }
                for tool in tools
            ]
        
        # Build request parameters
        request_params = {
            "model": kwargs.get("model", "gpt-4"),
            "messages": [
                {k: v for k, v in message.items() if k != "metadata"}
                for message in messages
            ],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4000),
        }
        
        # Only include tools and tool_choice if tools are provided
        if tools_param:
            request_params["tools"] = tools_param
            request_params["tool_choice"] = kwargs.get("tool_choice", "auto")
        
        response = await self.client.chat.completions.create(**request_params)
        
        message = response.choices[0].message.model_dump()
        return message

class AnthropicProvider(LLMProvider):
    """Provider implementation for Anthropic's API."""
    
    def __init__(self, api_key: str):
        """Initialize the Anthropic provider with API credentials."""
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      **kwargs) -> Message:
        """Generate a completion from Anthropic."""
        # Convert to Anthropic's message format
        anthropic_messages = []
        for message in messages:
            role = message.get("role", "user")
            if role == "system":
                # Skip for now, we'll add as system parameter
                continue
            
            content = message.get("content", "")
            anthropic_messages.append({"role": "user" if role == "user" else "assistant", "content": content})
        
        # Handle system message
        system_message = next((m.get("content", "") for m in messages if m.get("role") == "system"), "")
        
        # Handle tools
        tools_param = None
        if tools:
            tools_param = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": {
                        "type": "object",
                        "properties": tool.parameters,
                        "required": tool.required_parameters
                    }
                }
                for tool in tools
            ]
        
        # Build request parameters
        request_params = {
            "model": kwargs.get("model", "claude-3-opus-20240229"),
            "messages": anthropic_messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4000)
        }
        
        # Add system message if present
        if system_message:
            request_params["system"] = system_message
            
        # Add tools if provided
        if tools_param:
            request_params["tools"] = tools_param
        
        response = await self.client.messages.create(**request_params)
        
        # Convert Anthropic response to standard format
        content = response.content[0].text
        tool_calls = []
        
        if hasattr(response, "tool_use") and response.tool_use:
            for tool_use in response.tool_use:
                tool_calls.append({
                    "id": tool_use.id,
                    "type": "function",
                    "function": {
                        "name": tool_use.name,
                        "arguments": json.dumps(tool_use.input)
                    }
                })
        
        return {
            "role": "assistant",
            "content": content,
            "tool_calls": tool_calls if tool_calls else None
        }

class ProviderRegistry:
    """Registry for LLM providers."""
    
    _providers: Dict[str, LLMProvider] = {}
    
    @classmethod
    def register(cls, name: str, provider: LLMProvider) -> None:
        """Register a provider with the given name."""
        cls._providers[name] = provider
    
    @classmethod
    def get(cls, name: str) -> LLMProvider:
        """Get a provider by name."""
        if name not in cls._providers:
            raise ValueError(f"Provider {name} not registered")
        return cls._providers[name]
    
    @classmethod
    def list(cls) -> List[str]:
        """List all registered providers."""
        return list(cls._providers.keys()) 