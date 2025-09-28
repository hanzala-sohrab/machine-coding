# Multilevel Cache System

## Problem Statement

You are required to design and implement a **Multilevel Cache System** that stores key-value pairs of data. Both the `KEY` and `VALUE` are strings.

The cache system will have multiple levels, where **L1** is the top-most level and **Ln** is the last level. Each level can store a fixed number of items, and items may be evicted to lower levels when a level is full.

---

## Requirements

### Configuration

- The system starts with only **1 level** and can grow up to a configured **maximum number of levels**.
- Each level has a **fixed capacity** (number of items it can store). Different levels may have different capacities.

---

## Operations

### 1. READ `KEY`

- Start searching from **L1**.
- If the `KEY` is found:
  - Return the `VALUE`.
  - Promote this key-value pair to **L1** (respecting the write/eviction strategy).
- If not found in the current level, continue searching in the next level.
- If the key is not found in any level, return `None`.

---

### 2. WRITE `KEY VALUE`

- Always attempt to write in **L1**.
- If the level is full:
  - Evict an existing key-value pair using the configured **eviction strategy**.
  - Insert the evicted key-value pair into the **next level**.
  - If the next level is also full, repeat the eviction process recursively.
- If eviction reaches the **last level**:
  - Add a new level (if the maximum number of levels has not been reached).
  - Insert the evicted key-value pair into the new level.

---

### 3. DELETE `KEY`

- Remove the given `KEY` from **all levels** where it exists.

---

## Eviction Strategy

The eviction strategy should be **pluggable**.

For this implementation, use:

- **LFU (Least Frequently Used)**
  - Remove the key that has been used (read or written) the least number of times.
  - In case of ties, evict the least recently inserted key among them.

---

## Example

### Configuration

- Maximum levels = 3
- Capacities = [2, 3, 4] for L1, L2, and L3 respectively

### Operations

```text
WRITE a=1
WRITE b=2
WRITE c=3   → causes eviction from L1 to L2
READ b      → found in L2, promoted to L1
DELETE a    → deletes from all levels
```

### State of Cache

```text
L1: {b=2, c=3}
L2: {}
L3: {}
```

### Expected Interfaces

```python
class MultiLevelCache:
    def read(self, key: str) -> str | None:
        pass

    def write(self, key: str, value: str) -> None:
        pass

    def delete(self, key: str) -> None:
        pass
```

`CacheLevel`
Internal class implementing storage and LFU eviction for one level.

### Constraints

- 1 <= max_levels <= 10
- 1 <= capacity of each level <= 1000
- Keys and values are strings.

### Extensions

- Support other eviction strategies (e.g., LRU, FIFO).
- Make the cache thread-safe.
- Add persistence to disk for last-level storage.
