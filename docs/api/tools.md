# Tools API Reference

This document provides detailed API reference for the tool components of the Agent Framework framework.

## Base Tool Interface

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

## Built-in Tools

### `WebSearchTool`

Tool for searching the web.

```python
class WebSearchTool(Tool):
    def __init__(self, api_key: Optional[str] = None, search_engine: str = "google"):
        """
        Initialize the web search tool.
        
        Args:
            api_key: API key for the search engine. If None, will use environment variables.
            search_engine: Search engine to use. Currently supports "google" and "bing".
        """
        
    @property
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        return ToolSpec(
            name="web_search",
            description="Search the web for information.",
            parameters={
                "query": {
                    "type": "string",
                    "description": "The search query."
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return."
                }
            },
            required_parameters=["query"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Execute the web search.
        
        Args:
            parameters: Parameters for the search.
                - query: The search query.
                - num_results: Number of results to return. Default is 5.
                
        Returns:
            List of search results, each with "title", "url", and "snippet" fields.
        """
```

### `FileSystemTool`

Tool for interacting with the file system.

```python
class FileSystemTool(Tool):
    def __init__(self, base_dir: Optional[str] = None, allow_write: bool = False):
        """
        Initialize the file system tool.
        
        Args:
            base_dir: Base directory to restrict operations to. If None, will use the current directory.
            allow_write: Whether to allow write operations.
        """
        
    @property
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        return ToolSpec(
            name="filesystem",
            description="Interact with the file system.",
            parameters={
                "operation": {
                    "type": "string",
                    "description": "The operation to perform.",
                    "enum": ["read", "write", "list", "exists", "delete"]
                },
                "path": {
                    "type": "string",
                    "description": "The path to operate on."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write (for write operation)."
                }
            },
            required_parameters=["operation", "path"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """
        Execute the file system operation.
        
        Args:
            parameters: Parameters for the operation.
                - operation: The operation to perform.
                - path: The path to operate on.
                - content: The content to write (for write operation).
                
        Returns:
            Depends on the operation:
                - read: The file content as a string.
                - write: True if successful.
                - list: List of file names.
                - exists: Boolean indicating if the path exists.
                - delete: True if successful.
        """
```

### `ShellTool`

Tool for executing shell commands.

```python
class ShellTool(Tool):
    def __init__(self, allowed_commands: Optional[List[str]] = None, working_dir: Optional[str] = None):
        """
        Initialize the shell tool.
        
        Args:
            allowed_commands: List of allowed commands. If None, all commands are allowed.
            working_dir: Working directory for commands. If None, will use the current directory.
        """
        
    @property
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        return ToolSpec(
            name="shell",
            description="Execute shell commands.",
            parameters={
                "command": {
                    "type": "string",
                    "description": "The shell command to execute."
                }
            },
            required_parameters=["command"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the shell command.
        
        Args:
            parameters: Parameters for the command.
                - command: The shell command to execute.
                
        Returns:
            Dictionary with "stdout", "stderr", and "returncode" fields.
        """
```

### `DatabaseTool`

Tool for interacting with databases.

```python
class DatabaseTool(Tool):
    def __init__(self, connection_string: str, query_timeout: int = 30):
        """
        Initialize the database tool.
        
        Args:
            connection_string: Database connection string.
            query_timeout: Timeout for queries in seconds.
        """
        
    @property
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        return ToolSpec(
            name="database",
            description="Execute database queries.",
            parameters={
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute."
                },
                "params": {
                    "type": "object",
                    "description": "Parameters for the query."
                }
            },
            required_parameters=["query"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute the database query.
        
        Args:
            parameters: Parameters for the query.
                - query: The SQL query to execute.
                - params: Parameters for the query.
                
        Returns:
            List of rows, each as a dictionary of column names to values.
        """
```

### `APITool`

Tool for making API requests.

```python
class APITool(Tool):
    def __init__(self, base_url: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the API tool.
        
        Args:
            base_url: Base URL for API requests. If provided, will be prepended to all paths.
            headers: Default headers to include in all requests.
        """
        
    @property
    def spec(self) -> ToolSpec:
        """Return the specification for this tool."""
        return ToolSpec(
            name="api",
            description="Make API requests.",
            parameters={
                "method": {
                    "type": "string",
                    "description": "The HTTP method.",
                    "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]
                },
                "url": {
                    "type": "string",
                    "description": "The URL or path to request."
                },
                "headers": {
                    "type": "object",
                    "description": "Headers to include in the request."
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters for the request."
                },
                "data": {
                    "type": "object",
                    "description": "Data to send in the request body."
                }
            },
            required_parameters=["method", "url"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the API request.
        
        Args:
            parameters: Parameters for the request.
                - method: The HTTP method.
                - url: The URL or path to request.
                - headers: Headers to include in the request.
                - params: Query parameters for the request.
                - data: Data to send in the request body.
                
        Returns:
            Dictionary with "status", "headers", and "body" fields.
        """
```

## Tool Registry

### `ToolRegistry`

Registry for tools.

```python
class ToolRegistry:
    @staticmethod
    def register(name: str, tool_class: Type[Tool]) -> None:
        """
        Register a tool class.
        
        Args:
            name: Name to register the tool under.
            tool_class: Tool class to register.
        """
        
    @staticmethod
    def get(name: str) -> Type[Tool]:
        """
        Get a tool class by name.
        
        Args:
            name: Name of the tool to get.
            
        Returns:
            The tool class.
            
        Raises:
            ValueError: If the tool is not registered.
        """
        
    @staticmethod
    def create(name: str, **kwargs) -> Tool:
        """
        Create a tool instance.
        
        Args:
            name: Name of the tool to create.
            **kwargs: Additional arguments to pass to the tool constructor.
            
        Returns:
            The tool instance.
            
        Raises:
            ValueError: If the tool is not registered.
        """
        
    @staticmethod
    def list() -> List[str]:
        """
        List all registered tools.
        
        Returns:
            List of registered tool names.
        """
```

## Utility Functions

```python
def register_default_tools() -> None:
    """Register the default tools with the registry."""
    
def get_tool(name: str, **kwargs) -> Tool:
    """
    Get a tool instance by name.
    
    Args:
        name: Name of the tool to get.
        **kwargs: Additional arguments to pass to the tool constructor.
        
    Returns:
        The tool instance.
    """
``` 