# Memory API Reference

This document provides detailed API reference for the memory components of the Agent Framework framework.

## Base Memory Interface

### `MemoryInterface`

Interface for memory systems used by agents.

```python
class MemoryInterface(ABC, Generic[T]):
    @abstractmethod
    async def add(self, item: T) -> None:
        """Add an item to memory."""
        pass
    
    @abstractmethod
    async def get(self, query: Any, **kwargs) -> List[T]:
        """Retrieve items from memory based on a query."""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all items from memory."""
        pass
```

## Memory Implementations

### `ConversationMemory`

Memory system for storing conversation history.

```python
class ConversationMemory(MemoryInterface[Message]):
    def __init__(self, max_messages: int = 100):
        """
        Initialize the conversation memory.
        
        Args:
            max_messages: Maximum number of messages to store.
        """
        
    async def add(self, message: Message) -> None:
        """
        Add a message to memory.
        
        Args:
            message: The message to add.
        """
        
    async def get(self, query: Optional[str] = None, limit: int = 10, **kwargs) -> List[Message]:
        """
        Retrieve messages from memory.
        
        Args:
            query: Optional query to filter messages. If None, returns the most recent messages.
            limit: Maximum number of messages to return.
            **kwargs: Additional parameters for the query.
            
        Returns:
            List of messages.
        """
        
    async def clear(self) -> None:
        """Clear all messages from memory."""
        
    async def get_conversation_summary(self) -> str:
        """
        Get a summary of the conversation.
        
        Returns:
            A summary of the conversation.
        """
```

### `VectorMemory`

Memory system using vector embeddings for semantic search.

```python
class VectorMemory(MemoryInterface[T]):
    def __init__(self, 
                embedding_model: str = "text-embedding-ada-002", 
                embedding_provider: str = "openai",
                vector_db: Optional[str] = None,
                vector_db_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the vector memory.
        
        Args:
            embedding_model: Model to use for embeddings.
            embedding_provider: Provider for the embedding model.
            vector_db: Vector database to use. If None, will use an in-memory database.
            vector_db_config: Configuration for the vector database.
        """
        
    async def add(self, item: T) -> None:
        """
        Add an item to memory.
        
        Args:
            item: The item to add.
        """
        
    async def get(self, query: str, limit: int = 5, threshold: float = 0.7, **kwargs) -> List[T]:
        """
        Retrieve items from memory based on semantic similarity.
        
        Args:
            query: Query to search for.
            limit: Maximum number of items to return.
            threshold: Minimum similarity threshold.
            **kwargs: Additional parameters for the query.
            
        Returns:
            List of items.
        """
        
    async def clear(self) -> None:
        """Clear all items from memory."""
        
    async def delete(self, item_id: str) -> bool:
        """
        Delete an item from memory.
        
        Args:
            item_id: ID of the item to delete.
            
        Returns:
            True if the item was deleted, False otherwise.
        """
```

### `KeyValueMemory`

Simple key-value memory system.

```python
class KeyValueMemory(MemoryInterface[Tuple[str, Any]]):
    def __init__(self, ttl: Optional[int] = None):
        """
        Initialize the key-value memory.
        
        Args:
            ttl: Time-to-live for items in seconds. If None, items never expire.
        """
        
    async def add(self, item: Tuple[str, Any]) -> None:
        """
        Add a key-value pair to memory.
        
        Args:
            item: Tuple of (key, value).
        """
        
    async def get(self, query: str, **kwargs) -> List[Tuple[str, Any]]:
        """
        Retrieve items from memory by key.
        
        Args:
            query: Key to retrieve. Can use glob patterns.
            **kwargs: Additional parameters for the query.
            
        Returns:
            List of (key, value) tuples.
        """
        
    async def clear(self) -> None:
        """Clear all items from memory."""
        
    async def set(self, key: str, value: Any) -> None:
        """
        Set a value for a key.
        
        Args:
            key: The key.
            value: The value.
        """
        
    async def delete(self, key: str) -> bool:
        """
        Delete a key-value pair.
        
        Args:
            key: The key to delete.
            
        Returns:
            True if the key was deleted, False otherwise.
        """
```

### `SQLMemory`

Memory system using SQL for structured data.

```python
class SQLMemory(MemoryInterface[Dict[str, Any]]):
    def __init__(self, 
                connection_string: str, 
                table_name: str,
                schema: Dict[str, str]):
        """
        Initialize the SQL memory.
        
        Args:
            connection_string: Database connection string.
            table_name: Name of the table to use.
            schema: Schema for the table, mapping column names to types.
        """
        
    async def add(self, item: Dict[str, Any]) -> None:
        """
        Add an item to memory.
        
        Args:
            item: Dictionary of column values.
        """
        
    async def get(self, query: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieve items from memory using SQL.
        
        Args:
            query: SQL query to execute.
            params: Parameters for the query.
            **kwargs: Additional parameters for the query.
            
        Returns:
            List of rows as dictionaries.
        """
        
    async def clear(self) -> None:
        """Clear all items from memory."""
        
    async def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a raw SQL query.
        
        Args:
            query: SQL query to execute.
            params: Parameters for the query.
            
        Returns:
            Query result.
        """
```

## Memory Factory

### `MemoryFactory`

Factory for creating memory instances.

```python
class MemoryFactory:
    @staticmethod
    def create(memory_type: str, **kwargs) -> MemoryInterface:
        """
        Create a memory instance.
        
        Args:
            memory_type: Type of memory to create.
            **kwargs: Additional arguments to pass to the memory constructor.
            
        Returns:
            The memory instance.
            
        Raises:
            ValueError: If the memory type is not supported.
        """
```

## Utility Functions

```python
def create_memory(memory_type: str, **kwargs) -> MemoryInterface:
    """
    Create a memory instance.
    
    Args:
        memory_type: Type of memory to create.
        **kwargs: Additional arguments to pass to the memory constructor.
        
    Returns:
        The memory instance.
    """
    
def get_default_memory_config(memory_type: str) -> Dict[str, Any]:
    """
    Get the default configuration for a memory type.
    
    Args:
        memory_type: Type of memory.
        
    Returns:
        Default configuration dictionary.
    """
``` 