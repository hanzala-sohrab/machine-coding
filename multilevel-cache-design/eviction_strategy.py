from collections import defaultdict, OrderedDict


class EvictionStrategy:
    def get(self, key): ...
    def put(self, key, value): ...
    def delete(self, key): ...


class LFUStrategy(EvictionStrategy):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_value = {}
        self.key_freq = {}
        self.freq_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def _update_freq(self, key):
        freq = self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_freq[key] += 1
        self.freq_keys[self.key_freq[key]][key] = None

    def get(self, key):
        if key not in self.key_value:
            return None
        self._update_freq(key)
        return self.key_value[key]

    def put(self, key, value):
        evicted_item = None
        if key in self.key_value:
            self.key_value[key] = value
            self._update_freq(key)
            return evicted_item

        if len(self.key_value) >= self.capacity:
            lfu_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
            evicted_item = (lfu_key, self.key_value[lfu_key])
            del self.key_value[lfu_key]
            del self.key_freq[lfu_key]
            if not self.freq_keys[self.min_freq]:
                del self.freq_keys[self.min_freq]

        self.key_value[key] = value
        self.key_freq[key] = 1
        self.freq_keys[1][key] = None
        self.min_freq = 1
        return evicted_item

    def delete(self, key):
        if key not in self.key_value:
            return
        freq = self.key_freq[key]
        del self.key_value[key]
        del self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if self.min_freq == freq:
                self.min_freq = min(self.freq_keys.keys(), default=0)
