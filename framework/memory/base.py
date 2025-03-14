"""
Base memory implementations for the AgentFlow framework.
"""
from typing import Any, Dict, Generic, List, Optional, TypeVar
from ..core.base import MemoryInterface, Message

T = TypeVar('T')

class SimpleMemory(MemoryInterface[T]):
    """A simple in-memory implementation of MemoryInterface."""
    
    def __init__(self):
        """Initialize an empty memory."""
        self._items: List[T] = []
    
    async def add(self, item: T) -> None:
        """Add an item to memory."""
        self._items.append(item)
    
    async def get(self, query: Any = None, **kwargs) -> List[T]:
        """Retrieve items from memory.
        
        If query is None, returns all items.
        Otherwise, returns items that match the query.
        Behavior depends on the specific implementation.
        """
        if query is None:
            return self._items.copy()
        
        # In the base class, we just return all items if a query is provided
        # Subclasses should override this to implement actual filtering
        return self._items.copy()
    
    async def clear(self) -> None:
        """Clear all items from memory."""
        self._items.clear()

class MessageMemory(SimpleMemory[Message]):
    """A memory for storing conversation messages."""
    
    async def get_conversation_history(self, max_messages: Optional[int] = None) -> List[Message]:
        """Get the conversation history.
        
        Args:
            max_messages: Maximum number of messages to return.
                If None, returns all messages.
        
        Returns:
            A list of messages, with the most recent last.
        """
        messages = await self.get()
        if max_messages is not None:
            return messages[-max_messages:]
        return messages
    
    async def get_system_message(self) -> Optional[Message]:
        """Get the system message from memory."""
        messages = await self.get()
        for message in messages:
            if message.get("role") == "system":
                return message
        return None

class MemoryFactory:
    """Factory for creating memory instances."""
    
    @staticmethod
    def create_memory(memory_type: str, **kwargs) -> MemoryInterface:
        """Create a memory instance of the specified type."""
        if memory_type == "simple":
            return SimpleMemory()
        elif memory_type == "message":
            return MessageMemory()
        else:
            raise ValueError(f"Unknown memory type: {memory_type}") 