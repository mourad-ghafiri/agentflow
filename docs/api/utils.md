# Utilities API Reference

This document provides detailed API reference for the utility components of the Agent Framework framework.

## Logging Utilities

### `Logger`

Logging utility for the framework.

```python
class Logger:
    @staticmethod
    def configure(level: str = "INFO", 
                 log_file: Optional[str] = None, 
                 format: Optional[str] = None) -> None:
        """
        Configure the logger.
        
        Args:
            level: Logging level.
            log_file: Path to log file. If None, logs to console only.
            format: Log format string.
        """
        
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name: Name of the logger.
            
        Returns:
            Logger instance.
        """
```

### `LoggingMiddleware`

Middleware for logging agent interactions.

```python
class LoggingMiddleware:
    def __init__(self, log_level: str = "INFO"):
        """
        Initialize the logging middleware.
        
        Args:
            log_level: Logging level.
        """
        
    async def process_input(self, agent: Agent, input_message: Union[str, Message]) -> Union[str, Message]:
        """
        Process an input message before it's sent to the agent.
        
        Args:
            agent: The agent.
            input_message: The input message.
            
        Returns:
            The processed input message.
        """
        
    async def process_output(self, agent: Agent, output_message: Any) -> Any:
        """
        Process an output message after it's received from the agent.
        
        Args:
            agent: The agent.
            output_message: The output message.
            
        Returns:
            The processed output message.
        """
```

## Serialization Utilities

### `Serializer`

Utility for serializing and deserializing objects.

```python
class Serializer:
    @staticmethod
    def serialize(obj: Any) -> Dict[str, Any]:
        """
        Serialize an object to a dictionary.
        
        Args:
            obj: Object to serialize.
            
        Returns:
            Serialized object as a dictionary.
        """
        
    @staticmethod
    def deserialize(data: Dict[str, Any], cls: Type[T]) -> T:
        """
        Deserialize a dictionary to an object.
        
        Args:
            data: Dictionary to deserialize.
            cls: Class to deserialize to.
            
        Returns:
            Deserialized object.
        """
        
    @staticmethod
    def to_json(obj: Any) -> str:
        """
        Serialize an object to a JSON string.
        
        Args:
            obj: Object to serialize.
            
        Returns:
            JSON string.
        """
        
    @staticmethod
    def from_json(json_str: str, cls: Type[T]) -> T:
        """
        Deserialize a JSON string to an object.
        
        Args:
            json_str: JSON string to deserialize.
            cls: Class to deserialize to.
            
        Returns:
            Deserialized object.
        """
```

## Configuration Utilities

### `ConfigLoader`

Utility for loading configuration files.

```python
class ConfigLoader:
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file.
        
        Args:
            file_path: Path to the YAML file.
            
        Returns:
            Configuration dictionary.
        """
        
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Load a JSON configuration file.
        
        Args:
            file_path: Path to the JSON file.
            
        Returns:
            Configuration dictionary.
        """
        
    @staticmethod
    def save_yaml(config: Dict[str, Any], file_path: str) -> None:
        """
        Save a configuration dictionary to a YAML file.
        
        Args:
            config: Configuration dictionary.
            file_path: Path to the YAML file.
        """
        
    @staticmethod
    def save_json(config: Dict[str, Any], file_path: str) -> None:
        """
        Save a configuration dictionary to a JSON file.
        
        Args:
            config: Configuration dictionary.
            file_path: Path to the JSON file.
        """
```

## Validation Utilities

### `Validator`

Utility for validating configurations and inputs.

```python
class Validator:
    @staticmethod
    def validate_config(config: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
        """
        Validate a configuration against a schema.
        
        Args:
            config: Configuration dictionary.
            schema: Schema dictionary.
            
        Returns:
            List of validation errors. Empty if valid.
        """
        
    @staticmethod
    def validate_agent_config(config: Dict[str, Any]) -> List[str]:
        """
        Validate an agent configuration.
        
        Args:
            config: Agent configuration dictionary.
            
        Returns:
            List of validation errors. Empty if valid.
        """
        
    @staticmethod
    def validate_orchestrator_config(config: Dict[str, Any]) -> List[str]:
        """
        Validate an orchestrator configuration.
        
        Args:
            config: Orchestrator configuration dictionary.
            
        Returns:
            List of validation errors. Empty if valid.
        """
        
    @staticmethod
    def validate_tool_spec(spec: Dict[str, Any]) -> List[str]:
        """
        Validate a tool specification.
        
        Args:
            spec: Tool specification dictionary.
            
        Returns:
            List of validation errors. Empty if valid.
        """
```

## Tokenization Utilities

### `Tokenizer`

Utility for tokenizing text.

```python
class Tokenizer:
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the tokenizer.
        
        Args:
            model: Model to use for tokenization.
        """
        
    def encode(self, text: str) -> List[int]:
        """
        Encode text to tokens.
        
        Args:
            text: Text to encode.
            
        Returns:
            List of token IDs.
        """
        
    def decode(self, tokens: List[int]) -> str:
        """
        Decode tokens to text.
        
        Args:
            tokens: List of token IDs.
            
        Returns:
            Decoded text.
        """
        
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in text.
        
        Args:
            text: Text to count tokens in.
            
        Returns:
            Number of tokens.
        """
        
    def truncate_text(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to a maximum number of tokens.
        
        Args:
            text: Text to truncate.
            max_tokens: Maximum number of tokens.
            
        Returns:
            Truncated text.
        """
```

## Prompt Utilities

### `PromptTemplate`

Template for generating prompts.

```python
class PromptTemplate:
    def __init__(self, template: str):
        """
        Initialize the prompt template.
        
        Args:
            template: Template string with placeholders.
        """
        
    def format(self, **kwargs) -> str:
        """
        Format the template with values.
        
        Args:
            **kwargs: Values for placeholders.
            
        Returns:
            Formatted prompt.
        """
        
    @staticmethod
    def from_file(file_path: str) -> "PromptTemplate":
        """
        Load a template from a file.
        
        Args:
            file_path: Path to the template file.
            
        Returns:
            Prompt template.
        """
```

### `PromptLibrary`

Library of prompt templates.

```python
class PromptLibrary:
    @staticmethod
    def get_template(template_name: str) -> PromptTemplate:
        """
        Get a template by name.
        
        Args:
            template_name: Name of the template.
            
        Returns:
            Prompt template.
            
        Raises:
            ValueError: If the template is not found.
        """
        
    @staticmethod
    def register_template(template_name: str, template: PromptTemplate) -> None:
        """
        Register a template.
        
        Args:
            template_name: Name to register the template under.
            template: Prompt template to register.
        """
        
    @staticmethod
    def list_templates() -> List[str]:
        """
        List all registered templates.
        
        Returns:
            List of template names.
        """
```

## Miscellaneous Utilities

### `AsyncUtils`

Utilities for asynchronous operations.

```python
class AsyncUtils:
    @staticmethod
    async def gather_with_concurrency(n: int, *tasks) -> List[Any]:
        """
        Run tasks with a concurrency limit.
        
        Args:
            n: Maximum number of concurrent tasks.
            *tasks: Tasks to run.
            
        Returns:
            List of task results.
        """
        
    @staticmethod
    async def retry(coro, max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0) -> Any:
        """
        Retry a coroutine with exponential backoff.
        
        Args:
            coro: Coroutine to retry.
            max_retries: Maximum number of retries.
            delay: Initial delay in seconds.
            backoff: Backoff factor.
            
        Returns:
            Result of the coroutine.
            
        Raises:
            Exception: If all retries fail.
        """
```

### `RateLimiter`

Utility for rate limiting API calls.

```python
class RateLimiter:
    def __init__(self, calls_per_minute: int):
        """
        Initialize the rate limiter.
        
        Args:
            calls_per_minute: Maximum number of calls per minute.
        """
        
    async def acquire(self) -> None:
        """
        Acquire a token for making a call.
        
        This method will block until a token is available.
        """
        
    async def __aenter__(self) -> "RateLimiter":
        """Enter the context manager."""
        
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
``` 