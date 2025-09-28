# Machine Coding Repository

This repository contains various machine coding exercises and implementations.

## Project Structure

machine-coding/
├── README.md # This file - project overview
├── .gitignore # Git ignore rules
├── multilevel-cache-design/ # Multilevel cache system implementation
│ ├── README.md # Detailed documentation for the cache system
│ ├── main.py # Example usage and demo
│ ├── multilevel_cache.py # Main cache implementation
│ ├── cache_level.py # Individual cache level implementation
│ ├── eviction_strategy.py # Eviction strategies (LRU, FIFO, etc.)
│ ├── pyproject.toml # Project configuration
│ └── **init**.py # Python package initialization
└── restaurant-booking-system-design/ # Restaurant booking system implementation
├── README.md # Detailed documentation for the booking system
├── main.py # Example usage and demo
├── booking_system.py # Main booking system implementation
├── models.py # Data models (Venue, Booking, etc.)
├── errors.py # Custom exception classes
├── demo.py # Demo scripts for testing
├── pyproject.toml # Project configuration
└── **init**.py # Python package initialization

## Featured Projects

### 1. Multilevel Cache System

#### Overview

The multilevel cache system is a sophisticated caching implementation that stores key-value pairs across multiple cache levels. It's designed to optimize data access patterns by keeping frequently accessed data in faster, higher-level caches while maintaining larger storage capacity in lower levels.

#### Key Features

- **Multi-level Architecture**: Supports configurable number of cache levels (L1, L2, ..., Ln)
- **Dynamic Level Management**: Automatically adds new levels when needed, up to a configured maximum
- **Flexible Eviction Strategies**: Implements various eviction policies (LRU, FIFO, etc.)
- **Promotion on Read**: Promotes accessed items to higher levels for faster future access
- **Cascading Eviction**: When a level is full, evicted items cascade down to lower levels
- **Comprehensive Operations**: Supports READ, WRITE, and DELETE operations

#### Core Operations

1. **READ KEY**: Searches from L1 to Ln, promotes found items to L1
2. **WRITE KEY VALUE**: Always writes to L1, cascades evictions through levels
3. **DELETE KEY**: Removes the key from all levels where it exists

#### Technical Implementation

- **Language**: Python 3.12+
- **Architecture**: Object-oriented design with clear separation of concerns
- **Dependencies**: No external dependencies - pure Python implementation
- **Testing**: Example usage provided in `main.py`

#### Getting Started

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

#### Example Usage

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

### 2. Restaurant Booking System

#### Overview

The restaurant booking system is a comprehensive in-memory booking platform similar to Zomato/DineOut. It supports restaurant registration, time slot management, restaurant search with multiple filters, and concurrency-safe table bookings. The system is designed to be modular and extensible for future enhancements like hotel bookings.

#### Key Features

- **Restaurant Management**: Register restaurants with metadata (name, city, area, cuisine, cost-for-two, etc.)
- **Time Slot Management**: Restaurant owners can publish available time slots with table counts
- **Advanced Search**: Search restaurants by multiple filters (city, area, cuisine, name, cost range, veg-only, etc.)
- **Concurrency-Safe Booking**: Thread-safe table booking using per-slot locking to prevent double-booking
- **Booking Window**: Configurable booking window (e.g., bookings allowed only up to 30 days in advance)
- **Error Handling**: Comprehensive exception handling with custom error types
- **Modular Design**: Clean separation of concerns for easy testing and extension

#### Core Operations

1. **Register Restaurant**: Add a new restaurant to the system
2. **Update Time Slots**: Set available time slots and table counts for a restaurant
3. **Search restaurants**: Find restaurants using various filters and custom criteria
4. **Book Table**: Reserve a table for a specific time slot with concurrency protection

#### Technical Implementation

- **Language**: Python 3.12+
- **Architecture**: Object-oriented design with threading support
- **Concurrency**: Uses reentrant locks and per-slot locking for thread safety
- **Dependencies**: No external dependencies - pure Python implementation
- **Testing**: Comprehensive demo scripts in `demo.py`

#### Getting Started

1. Navigate to the restaurant booking system project:

   ```bash
   cd restaurant-booking-system-design
   ```

2. Install dependencies:

   ```bash
   uv sync
   # or
   pip install -e .
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

#### Example Usage

```python
from booking_system import BookingSystem
from models import Venue
from datetime import datetime, date, timedelta

# Initialize booking system
system = BookingSystem(booking_window_days=30)

# Register a restaurant
venue = Venue(
    id="venue_123",
    name="Italian Bistro",
    city="New York",
    area="Manhattan",
    cuisine="Italian",
    is_veg=False,
    cost_for_two=100
)
system.register_venue(venue)

# Set up time slots
tomorrow = date.today() + timedelta(days=1)
slot_dt = datetime.combine(tomorrow, datetime.min.time().replace(hour=20))
system.update_time_slots(venue.id, [slot_dt], tables_each=5)

# Search restaurants
results = system.search_venues(city="New York", cuisine="Italian")

# Book a table
booking = system.book_table("user_456", venue.id, slot_dt, num_people=4)
```
