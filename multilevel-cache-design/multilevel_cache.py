"""
A multilevel cache implementation that manages multiple cache levels with different capacities.

The cache follows a hierarchical structure where:
- Level 1 (L1) is the smallest but fastest cache
- Higher levels (L2, L3, etc.) are larger but slower
- Frequently accessed items are promoted to faster levels
- Evicted items cascade down to slower levels

Attributes:
    levels (list): List of CacheLevel objects representing each cache level
    max_levels (int): Maximum number of cache levels allowed
    capacities (list): List of capacities for each level
    strategy_cls (Type[EvictionStrategy]): Eviction strategy class to use for all levels
"""

from typing import Type
from cache_level import CacheLevel
from eviction_strategy import EvictionStrategy, LFUStrategy


class MultiLevelCache:
    def __init__(
        self,
        max_levels: int,
        capacities: list[int],
        strategy_cls: Type[EvictionStrategy] = LFUStrategy,
    ):
        """
        Initialize the multilevel cache.

        Args:
            max_levels: Maximum number of cache levels that can be created
            capacities: List of capacities for each level (index corresponds to level number)
            strategy_cls: Eviction strategy class to use (defaults to LFUStrategy)
        """
        self.levels = []
        self.max_levels = max_levels
        self.capacities = capacities
        self.strategy_cls = strategy_cls
        # Create the first cache level with the specified capacity
        self.levels.append(CacheLevel(capacities[0], strategy_cls))

    def read(self, key: str):
        """
        Read a value from the cache.

        Implements a read-through strategy with promotion:
        1. Searches from L1 (fastest) to Ln (slowest)
        2. If found in L1, returns immediately
        3. If found in Li (i > 0), promotes the item to L1 and returns value
        4. If not found in any level, returns None

        Args:
            key: The key to search for

        Returns:
            The value associated with the key, or None if not found
        """
        # Search through each level starting from L1 (fastest)
        for i, level in enumerate(self.levels):
            value = level.get(key)
            if value is not None:
                # Cache hit: if found in a level other than L1, promote it to L1
                if i != 0:
                    self.write(key, value)
                return value
        # Cache miss: key not found in any level
        return None

    def write(self, key: str, value: str):
        """
        Write a key-value pair to the cache.

        Implements a write-through with cascading eviction:
        1. Attempts to write to L1 first
        2. If L1 is full, evicts an item and writes it to L2
        3. Continues cascading evicted items down the levels
        4. If last level is full and max_levels not reached, creates a new level

        Args:
            key: The key to write
            value: The value to associate with the key
        """
        # Start with the item to be written
        evicted = (key, value)

        # Try to write to each existing level, cascading evicted items
        for level in self.levels:
            evicted = level.put(*evicted)
            if evicted is None:
                # Item was successfully placed in this level, no eviction needed
                return

        # If we get here, all levels are full and we have an evicted item
        # Check if we can create a new level
        if len(self.levels) < self.max_levels:
            # Create a new level with the next capacity in the list
            new_capacity = self.capacities[len(self.levels)]
            new_level = CacheLevel(new_capacity, self.strategy_cls)
            self.levels.append(new_level)
            # Place the evicted item in the new level
            new_level.put(*evicted)

    def delete(self, key: str):
        """
        Delete a key from all cache levels.

        Implements a delete-through strategy to maintain consistency:
        Removes the key from all levels to ensure no stale data remains.

        Args:
            key: The key to delete from all levels
        """
        # Remove the key from every cache level
        for level in self.levels:
            level.delete(key)

    def __str__(self):
        """
        Return a string representation of the multilevel cache.

        Returns:
            A formatted string showing the contents of each cache level
        """
        # Create a formatted string showing each level's contents
        return "\n".join([f"L{i+1}: {level}" for i, level in enumerate(self.levels)])
