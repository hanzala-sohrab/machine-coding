"""
Eviction strategy implementations for cache management.

This module provides abstract and concrete implementations of cache eviction
strategies. The LFU (Least Frequently Used) strategy is implemented here,
which evicts items that are accessed least frequently when the cache is full.

Key Components:
- EvictionStrategy: Abstract base class defining the cache interface
- LFUStrategy: Concrete implementation using Least Frequently Used algorithm
"""

from collections import defaultdict, OrderedDict
from typing import Optional, Any, Union


class EvictionStrategy:
    """
    Abstract base class defining the interface for cache eviction strategies.

    All concrete eviction strategies must implement these three core operations:
    - get: Retrieve a value from cache
    - put: Add/update a value in cache
    - delete: Remove a value from cache

    This class uses abstract methods to ensure consistent interface across
    different eviction algorithms (LFU, LRU, FIFO, etc.).
    """

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.

        Args:
            key: The key to look up in the cache

        Returns:
            The value associated with the key, or None if not found
        """
        ...

    def put(self, key: str, value: str) -> Optional[tuple]:
        """
        Add or update a key-value pair in the cache.

        Args:
            key: The key to add or update
            value: The value to associate with the key

        Returns:
            A tuple (evicted_key, evicted_value) if an item was evicted,
            or None if no eviction was necessary
        """
        ...

    def delete(self, key: str) -> None:
        """
        Remove a key-value pair from the cache.

        Args:
            key: The key to remove from the cache
        """
        ...


class LFUStrategy(EvictionStrategy):
    """
    Least Frequently Used (LFU) cache eviction strategy.

    This strategy tracks how often each key is accessed and evicts the
    least frequently used items when the cache reaches capacity. Items
    with the same access frequency are evicted in insertion order (FIFO).

    Data Structures:
    - key_value: Dict storing key -> value mappings
    - key_freq: Dict storing key -> access frequency mappings
    - freq_keys: defaultdict of OrderedDicts storing frequency -> {keys} mappings
    - min_freq: Integer tracking the minimum access frequency in the cache

    The use of OrderedDict within freq_keys ensures that when multiple keys
    have the same frequency, they are evicted in FIFO order.
    """

    def __init__(self, capacity: int):
        """
        Initialize the LFU strategy with the specified capacity.

        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        # Store key-value pairs
        self.key_value = {}
        # Store key -> frequency mappings
        self.key_freq = {}
        # Store frequency -> OrderedDict of keys (for FIFO eviction within same frequency)
        self.freq_keys = defaultdict(OrderedDict)
        # Track the minimum frequency in the cache
        self.min_freq = 0

    def _update_freq(self, key: str) -> None:
        """
        Update the access frequency for a key.

        This internal method is called when a key is accessed (get or put).
        It moves the key from its current frequency bucket to the next higher
        frequency bucket and updates the minimum frequency if necessary.

        Args:
            key: The key whose frequency should be updated
        """
        # Get the current frequency of the key
        freq = self.key_freq[key]

        # Remove the key from its current frequency bucket
        del self.freq_keys[freq][key]

        # If this frequency bucket is now empty, clean it up
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            # If we removed the min_freq bucket, increment min_freq
            if self.min_freq == freq:
                self.min_freq += 1

        # Increment the key's frequency and add it to the new bucket
        self.key_freq[key] += 1
        self.freq_keys[self.key_freq[key]][key] = None

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache and update its access frequency.

        Args:
            key: The key to look up in the cache

        Returns:
            The value associated with the key, or None if not found
        """
        # Cache miss: key not found
        if key not in self.key_value:
            return None

        # Cache hit: update the key's frequency and return the value
        self._update_freq(key)
        return self.key_value[key]

    def put(self, key: str, value: str) -> Optional[tuple]:
        """
        Add or update a key-value pair in the cache.

        If the key already exists, update its value and frequency.
        If the key is new and cache is full, evict the least frequently used item.

        Args:
            key: The key to add or update
            value: The value to associate with the key

        Returns:
            A tuple (evicted_key, evicted_value) if an item was evicted,
            or None if no eviction was necessary
        """
        evicted_item = None

        # Case 1: Key already exists - update value and frequency
        if key in self.key_value:
            self.key_value[key] = value
            self._update_freq(key)
            return evicted_item  # No eviction needed for updates

        # Case 2: Key is new - check if cache is full
        if len(self.key_value) >= self.capacity:
            # Evict the least frequently used item
            # Get the first key from the min_freq bucket (FIFO order)
            lfu_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
            evicted_item = (lfu_key, self.key_value[lfu_key])

            # Clean up the evicted key from all data structures
            del self.key_value[lfu_key]
            del self.key_freq[lfu_key]

            # Clean up the frequency bucket if it's now empty
            if not self.freq_keys[self.min_freq]:
                del self.freq_keys[self.min_freq]

        # Add the new key-value pair
        self.key_value[key] = value
        self.key_freq[key] = 1  # New keys start with frequency 1
        self.freq_keys[1][key] = None  # Add to frequency-1 bucket
        self.min_freq = 1  # New key has minimum frequency

        return evicted_item

    def delete(self, key: str) -> None:
        """
        Remove a key-value pair from the cache.

        Cleans up the key from all internal data structures and updates
        the minimum frequency if necessary.

        Args:
            key: The key to remove from the cache
        """
        # Key doesn't exist, nothing to do
        if key not in self.key_value:
            return

        # Get the key's frequency before deletion
        freq = self.key_freq[key]

        # Remove the key from all data structures
        del self.key_value[key]
        del self.key_freq[key]
        del self.freq_keys[freq][key]

        # Clean up the frequency bucket if it's now empty
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            # If we deleted the min_freq bucket, find the new minimum
            if self.min_freq == freq:
                self.min_freq = min(self.freq_keys.keys(), default=0)
