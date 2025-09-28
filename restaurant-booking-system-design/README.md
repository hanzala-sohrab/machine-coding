# Restaurant Booking System

## Overview

Design and implement a simple **in-memory** restaurant booking system (like Zomato / DineOut) that supports:

- **Registering restaurants** (owners can register and publish available time slots)
- **Searching restaurants** by filters (city, area, cuisine, name, cost-for-two, veg/non-veg, …)
- **Booking a table** for `n` people for a 1-hour slot (bookings allowed only up to `m` days in future)

This repository contains a modular, object-oriented Python implementation that demonstrates the core system, concurrency-safe booking, and example demos. The code is intentionally **DB-less** (in-memory) to meet the problem constraints but is designed so interfaces can be adapted later for persistence or hotel bookings.

---

## Key Requirements (P0)

- Library / interfaces must be generic enough to extend (e.g., hotels later).
- Provide working code that demonstrates `registerRestaurant`, `updateTimeSlots`, `searchRestaurant`, and `bookTable`.
- Good error handling and clear exceptions.
- Concurrency handling for parallel booking attempts (prevent double-booking).
- No databases, no web APIs required — a `main()` or demo script is sufficient.
- Evaluation criteria: separation of concerns, abstractions, OO principles, testability, readability, language proficiency.

---

## Features

- Register restaurants with metadata: `name`, `city`, `area`, `cuisine`, `is_veg`, `cost_for_two`, etc.
- Owners can **publish time slots** (1-hour slots) and indicate number of available tables per slot.
- Users can **search** restaurants by multiple filters and optional custom filters.
- Users can **book** a table for `n` people at a specific datetime slot (one booking consumes one table).
- Bookings allowed only up to `m` days into the future (configurable).
- Concurrency-safe booking using per-slot locking to handle parallel bookings.
- Clear exception types for `ValidationError`, `SlotUnavailableError`, `NotFoundError`, etc.
- Modular code for easy testing and extension.

---

## Public API / Function Signatures (examples)

```python
# Register a restaurant (returns restaurant_id)
registerRestaurant(name: str, city: str, area: str, **meta) -> str

# Update time slots for a restaurant
# slot_datetimes: List[datetime], tables_each: int
updateTimeSlots(restaurant_id: str, slot_datetimes: List[datetime], tables_each: int) -> None

# Search restaurants (many optional filters)
searchRestaurant(
    logged_in_user_id: str,
    city: Optional[str] = None,
    area: Optional[str] = None,
    cuisine: Optional[str] = None,
    name: Optional[str] = None,
    cost_for_two_min: Optional[int] = None,
    cost_for_two_max: Optional[int] = None,
    veg_only: Optional[bool] = None,
    extra_filter: Optional[Callable] = None
) -> List[Dict]

# Book a table
bookTable(user_id: str, restaurant_id: str, slot_dt: datetime, no_of_people: int) -> Booking

# Optional helpers
listBookings() -> List[Booking]
getRestaurant(restaurant_id: str) -> Restaurant
```
