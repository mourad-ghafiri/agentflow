# Providers API Reference

This document provides detailed API reference for the provider components of the Agent Framework framework.

## Base Provider Interface

### `LLMProvider`

Abstract interface for LLM providers.

```python
class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      **kwargs) -> Message:
        """Generate a completion from the LLM."""
        pass
```

## Provider Implementations

### `OpenAIProvider`

Provider implementation for OpenAI models.

```python
class OpenAIProvider(LLMProvider):
    def __init__(self, 
                api_key: Optional[str] = None, 
                organization: Optional[str] = None,
                default_model: str = "gpt-4o"):
        """
        Initialize the OpenAI provider.
        
        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
            organization: OpenAI organization ID. If None, will use OPENAI_ORGANIZATION environment variable.
            default_model: Default model to use if not specified in the request.
        """
        
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      model: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      **kwargs) -> Message:
        """
        Generate a completion from OpenAI.
        
        Args:
            messages: List of messages in the conversation.
            tools: Optional list of tool specifications.
            model: Model to use. If None, will use the default model.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters to pass to the OpenAI API.
            
        Returns:
            The generated message.
        """
```

### `AnthropicProvider`

Provider implementation for Anthropic models.

```python
class AnthropicProvider(LLMProvider):
    def __init__(self, 
                api_key: Optional[str] = None,
                default_model: str = "claude-3-opus-20240229"):
        """
        Initialize the Anthropic provider.
        
        Args:
            api_key: Anthropic API key. If None, will use ANTHROPIC_API_KEY environment variable.
            default_model: Default model to use if not specified in the request.
        """
        
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      model: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      **kwargs) -> Message:
        """
        Generate a completion from Anthropic.
        
        Args:
            messages: List of messages in the conversation.
            tools: Optional list of tool specifications.
            model: Model to use. If None, will use the default model.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters to pass to the Anthropic API.
            
        Returns:
            The generated message.
        """
```

### `HuggingFaceProvider`

Provider implementation for Hugging Face models.

```python
class HuggingFaceProvider(LLMProvider):
    def __init__(self, 
                api_key: Optional[str] = None,
                default_model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        """
        Initialize the Hugging Face provider.
        
        Args:
            api_key: Hugging Face API key. If None, will use HF_API_KEY environment variable.
            default_model: Default model to use if not specified in the request.
        """
        
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      model: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      **kwargs) -> Message:
        """
        Generate a completion from Hugging Face.
        
        Args:
            messages: List of messages in the conversation.
            tools: Optional list of tool specifications.
            model: Model to use. If None, will use the default model.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters to pass to the Hugging Face API.
            
        Returns:
            The generated message.
        """
```

### `LocalProvider`

Provider implementation for local models.

```python
class LocalProvider(LLMProvider):
    def __init__(self, 
                model_path: str,
                device: str = "cuda",
                context_length: int = 4096):
        """
        Initialize the local provider.
        
        Args:
            model_path: Path to the model weights.
            device: Device to run the model on.
            context_length: Maximum context length for the model.
        """
        
    async def complete(self, 
                      messages: List[Message], 
                      tools: Optional[List[ToolSpec]] = None, 
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      **kwargs) -> Message:
        """
        Generate a completion from a local model.
        
        Args:
            messages: List of messages in the conversation.
            tools: Optional list of tool specifications.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters to pass to the model.
            
        Returns:
            The generated message.
        """
```

## Provider Registry

### `ProviderRegistry`

Registry for LLM providers.

```python
class ProviderRegistry:
    @staticmethod
    def register(name: str, provider_class: Type[LLMProvider]) -> None:
        """
        Register a provider class.
        
        Args:
            name: Name to register the provider under.
            provider_class: Provider class to register.
        """
        
    @staticmethod
    def get(name: str) -> Type[LLMProvider]:
        """
        Get a provider class by name.
        
        Args:
            name: Name of the provider to get.
            
        Returns:
            The provider class.
            
        Raises:
            ValueError: If the provider is not registered.
        """
        
    @staticmethod
    def create(name: str, **kwargs) -> LLMProvider:
        """
        Create a provider instance.
        
        Args:
            name: Name of the provider to create.
            **kwargs: Additional arguments to pass to the provider constructor.
            
        Returns:
            The provider instance.
            
        Raises:
            ValueError: If the provider is not registered.
        """
        
    @staticmethod
    def list() -> List[str]:
        """
        List all registered providers.
        
        Returns:
            List of registered provider names.
        """
```

## Utility Functions

```python
def register_default_providers() -> None:
    """Register the default providers with the registry."""
    
def get_provider(name: str, **kwargs) -> LLMProvider:
    """
    Get a provider instance by name.
    
    Args:
        name: Name of the provider to get.
        **kwargs: Additional arguments to pass to the provider constructor.
        
    Returns:
        The provider instance.
    """
``` 