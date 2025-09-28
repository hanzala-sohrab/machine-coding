"""
A wrapper class for a single cache level that uses a specific eviction strategy.

This class provides a clean interface for cache operations while delegating
the actual implementation to an underlying eviction strategy. It acts as a
bridge between the multilevel cache orchestrator and the specific eviction
algorithm (e.g., LFU, LRU, FIFO).

Attributes:
    strategy (EvictionStrategy): The underlying eviction strategy instance
"""

from typing import Type, Optional, Any
from eviction_strategy import EvictionStrategy


class CacheLevel:
    """
    Initialize a cache level with the specified capacity and eviction strategy.

    Args:
        capacity: The maximum number of items this cache level can hold
        strategy_cls: The class of evacuate strategy to use (e.g., LFUStrategy)
    """

    def __init__(self, capacity: int, strategy_cls: Type[EvictionStrategy]):
        # Create an instance of the specified evacuate strategy with the given capacity
        self.strategy = strategy_cls(capacity)

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache level.

        Delegates the get operation to the underlying evacuate strategy.
        The strategy may update internal state (e.g., access frequency for LFU).

        Args:
            key: The key to look up in the cache

        Returns:
            The value associated with the key, or None if the key is not found
        """
        return self.strategy.get(key)

    def put(self, key: str, value: str) -> Optional[tuple]:
        """
        Add or update a key-value pair in the cache level.

        Delegates the put operation to the underlying evacuate strategy.
        If the cache is full, the strategy will evict an item according to its
        algorithm and return the evicted key-value pair.

        Args:
            key: The key to add or update
            value: The value to associate with the key

        Returns:
            A tuple (evicted_key, evicted_value) if an item was evicted,
            or None if no evict was necessary
        """
        return self.strategy.put(key, value)

    def delete(self, key: str) -> None:
        """
        Remove a key-value pair from the cache level.

        Delegates the delete operation to the underlying evacuate strategy.
        The strategy will clean up any internal state associated with the key.

        Args:
            key: The key to remove from the cache
        """
        self.strategy.delete(key)

    def __str__(self) -> str:
        """
        Return a string representation of the cache level's contents.

        Provides a readable view of the current state of this cache level,
        showing all key-value pairs stored in the underlying strategy.

        Returns:
            A string representation of the cache contents (typically a dict string)
        """
        return str(self.strategy.key_value)
