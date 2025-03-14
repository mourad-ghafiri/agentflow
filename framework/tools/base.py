"""
Base tool implementations for the AgentFlow framework.
"""
import inspect
import json
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Type, get_type_hints, Callable, Union
from pydantic import BaseModel, create_model, Field

from ..core.base import Tool, ToolSpec

class BaseTool(Tool):
    """Base implementation of the Tool interface."""
    
    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description
        self._spec = self._build_spec()
    
    def _build_spec(self) -> ToolSpec:
        """Build a ToolSpec from the tool's implementation."""
        execute_method = getattr(self.__class__, "execute", None)
        if not execute_method:
            raise ValueError(f"Tool {self._name} must implement execute method")
        
        signature = inspect.signature(execute_method)
        parameters = {}
        required_parameters = []
        
        # Get the first parameter (after self)
        param_names = list(signature.parameters.keys())
        if len(param_names) < 2:
            raise ValueError(f"Tool {self._name} execute method must accept parameters dict")
        
        # Get type hints and build parameters
        hints = get_type_hints(execute_method)
        return_type = hints.get('return')
        
        return ToolSpec(
            name=self._name,
            description=self._description,
            parameters={},  # Must be overridden by subclasses
            required_parameters=[],  # Must be overridden by subclasses
            return_type=str(return_type) if return_type else None
        )
    
    @property
    def spec(self) -> ToolSpec:
        """Return the tool's specification."""
        return self._spec

class FunctionTool(BaseTool):
    """A tool that wraps a function."""
    
    def __init__(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """Initialize a tool from a function."""
        self.func = func
        name = name or func.__name__
        description = description or func.__doc__ or f"Execute the {name} function"
        super().__init__(name, description)
        
        # Override the spec with function parameters
        self._spec = self._build_func_spec()
    
    def _build_func_spec(self) -> ToolSpec:
        """Build a ToolSpec from the wrapped function."""
        signature = inspect.signature(self.func)
        parameters = {}
        required_parameters = []
        
        for param_name, param in signature.parameters.items():
            # Determine if parameter is required
            if param.default is inspect.Parameter.empty:
                required_parameters.append(param_name)
            
            # Try to infer parameter type
            param_type = "string"
            if param.annotation is not inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list or param.annotation == List:
                    param_type = "array"
                elif param.annotation == dict or param.annotation == Dict:
                    param_type = "object"
            
            parameters[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name} for function {self.func.__name__}"
            }
        
        # Get return type
        hints = get_type_hints(self.func)
        return_type = hints.get('return')
        
        return ToolSpec(
            name=self._name,
            description=self._description,
            parameters=parameters,
            required_parameters=required_parameters,
            return_type=str(return_type) if return_type else None
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the wrapped function with the given parameters."""
        # Check required parameters
        for param in self._spec.required_parameters:
            if param not in parameters:
                raise ValueError(f"Required parameter {param} missing")
        
        # Execute the function
        if inspect.iscoroutinefunction(self.func):
            return await self.func(**parameters)
        else:
            return self.func(**parameters)

class PydanticTool(BaseTool):
    """A tool that uses Pydantic models for input and output validation."""
    
    def __init__(self, 
                name: str, 
                description: str, 
                input_model: Type[BaseModel], 
                output_model: Optional[Type[BaseModel]] = None):
        """Initialize with Pydantic models for input and output."""
        self.input_model = input_model
        self.output_model = output_model
        super().__init__(name, description)
        
        # Override the spec with Pydantic model
        self._spec = self._build_pydantic_spec()
    
    def _build_pydantic_spec(self) -> ToolSpec:
        """Build a ToolSpec from the Pydantic models."""
        schema = self.input_model.model_json_schema()
        
        parameters = schema.get("properties", {})
        required_parameters = schema.get("required", [])
        
        # Get return type
        return_type = None
        if self.output_model:
            return_type = self.output_model.__name__
        
        return ToolSpec(
            name=self._name,
            description=self._description,
            parameters=parameters,
            required_parameters=required_parameters,
            return_type=return_type
        )
    
    @abstractmethod
    async def _execute_with_validated_input(self, validated_input: BaseModel) -> Any:
        """Execute the tool with validated input."""
        pass
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the tool with the given parameters."""
        # Validate input
        validated_input = self.input_model(**parameters)
        
        # Execute with validated input
        result = await self._execute_with_validated_input(validated_input)
        
        # Validate output if output model exists
        if self.output_model and not isinstance(result, self.output_model):
            if isinstance(result, dict):
                result = self.output_model(**result)
            else:
                raise ValueError(f"Result {result} is not compatible with output model {self.output_model}")
        
        return result

class ToolRegistry:
    """Registry for tools."""
    
    _tools: Dict[str, Tool] = {}
    
    @classmethod
    def register(cls, tool: Tool) -> None:
        """Register a tool."""
        cls._tools[tool.spec.name] = tool
    
    @classmethod
    def get(cls, name: str) -> Tool:
        """Get a tool by name."""
        if name not in cls._tools:
            raise ValueError(f"Tool {name} not registered")
        return cls._tools[name]
    
    @classmethod
    def list_specs(cls) -> List[ToolSpec]:
        """List all registered tool specifications."""
        return [tool.spec for tool in cls._tools.values()]
    
    @classmethod
    def list_names(cls) -> List[str]:
        """List all registered tool names."""
        return list(cls._tools.keys()) 