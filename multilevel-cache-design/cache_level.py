from typing import Type
from eviction_strategy import EvictionStrategy


class CacheLevel:
    def __init__(self, capacity: int, strategy_cls: Type[EvictionStrategy]):
        self.strategy = strategy_cls(capacity)

    def get(self, key: str):
        return self.strategy.get(key)

    def put(self, key: str, value: str):
        return self.strategy.put(key, value)

    def delete(self, key: str):
        self.strategy.delete(key)

    def __str__(self):
        return str(self.strategy.key_value)
