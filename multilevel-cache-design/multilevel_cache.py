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
        self.levels: list[CacheLevel] = []
        self.max_levels = max_levels
        self.capacities = capacities
        self.strategy_cls = strategy_cls
        self.levels.append(CacheLevel(capacities[0], strategy_cls))

    def read(self, key: str):
        for i, level in enumerate(self.levels):
            value = level.get(key)
            if value is not None:
                if i != 0:
                    self.write(key, value)
                return value
        return None

    def write(self, key: str, value: str):
        evicted = (key, value)
        for level in self.levels:
            evicted = level.put(*evicted)
            if evicted is None:
                return
        if len(self.levels) < self.max_levels:
            new_capacity = self.capacities[len(self.levels)]
            new_level = CacheLevel(new_capacity, self.strategy_cls)
            self.levels.append(new_level)
            new_level.put(*evicted)

    def delete(self, key: str):
        for level in self.levels:
            level.delete(key)

    def __str__(self):
        return "\n".join([f"L{i+1}: {level}" for i, level in enumerate(self.levels)])
