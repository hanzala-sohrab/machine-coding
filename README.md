# Machine Coding Repository

This repository contains various machine coding exercises and implementations.

## Project Structure

```
machine-coding/
├── README.md                    # This file - project overview
├── .gitignore                   # Git ignore rules
└── multilevel-cache-design/     # Multilevel cache system implementation
    ├── README.md               # Detailed documentation for the cache system
    ├── main.py                 # Example usage and demo
    ├── multilevel_cache.py     # Main cache implementation
    ├── cache_level.py          # Individual cache level implementation
    ├── eviction_strategy.py    # Eviction strategies (LRU, FIFO, etc.)
    ├── pyproject.toml          # Project configuration
    └── __init__.py             # Python package initialization
```

## Featured Project: Multilevel Cache System

### Overview

The multilevel cache system is a sophisticated caching implementation that stores key-value pairs across multiple cache levels. It's designed to optimize data access patterns by keeping frequently accessed data in faster, higher-level caches while maintaining larger storage capacity in lower levels.

### Key Features

- **Multi-level Architecture**: Supports configurable number of cache levels (L1, L2, ..., Ln)
- **Dynamic Level Management**: Automatically adds new levels when needed, up to a configured maximum
- **Flexible Eviction Strategies**: Implements various eviction policies (LRU, FIFO, etc.)
- **Promotion on Read**: Promotes accessed items to higher levels for faster future access
- **Cascading Eviction**: When a level is full, evicted items cascade down to lower levels
- **Comprehensive Operations**: Supports READ, WRITE, and DELETE operations

### Core Operations

1. **READ KEY**: Searches from L1 to Ln, promotes found items to L1
2. **WRITE KEY VALUE**: Always writes to L1, cascades evictions through levels
3. **DELETE KEY**: Removes the key from all levels where it exists

### Technical Implementation

- **Language**: Python 3.12+
- **Architecture**: Object-oriented design with clear separation of concerns
- **Dependencies**: No external dependencies - pure Python implementation
- **Testing**: Example usage provided in `main.py`

## Getting Started

### Prerequisites

- Python 3.12 or higher
- `uv` package manager (recommended) or pip

### Setup

1. Navigate to the multilevel cache project:

   ```bash
   cd multilevel-cache-design
   ```

2. Install dependencies:

   ```bash
   uv sync
   # or
   pip install -e .
   ```

3. Run the example:
   ```bash
   python main.py
   ```

### Example Usage

```python
from multilevel_cache import MultiLevelCache

# Initialize cache with 3 levels and capacities [2, 3, 4]
cache = MultiLevelCache(max_levels=3, capacities=[2, 3, 4])

# Write key-value pairs
cache.write("a", "1")
cache.write("b", "2")
cache.write("c", "3")

# Read values (promotes to L1)
value = cache.read("b")

# Delete keys from all levels
cache.delete("a")
```

## Documentation

For detailed documentation of the multilevel cache system, including:

- Complete problem statement
- Detailed requirements
- Implementation details
- API reference

Please refer to the [multilevel-cache-design/README.md](multilevel-cache-design/README.md) file.

## Learning Objectives

This implementation demonstrates several important computer science concepts:

- **Cache Hierarchies**: Understanding multi-level cache systems
- **Eviction Algorithms**: Implementing LRU, FIFO, and other strategies
- **Data Structures**: Efficient storage and retrieval mechanisms
- **System Design**: Scalable and maintainable architecture
- **Algorithm Design**: Complex operation handling with edge cases

## Contributing

This repository is intended for learning and demonstration purposes. Feel free to:

1. Explore the implementations
2. Run the examples
3. Modify and experiment with the code
4. Add new features or improvements

## License

This project is for educational purposes. Feel free to use and modify the code for learning.
