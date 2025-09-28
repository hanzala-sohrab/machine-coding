"""
Models for the restaurant booking system.

This module contains dataclasses and classes that represent the core
entities of the system: bookings and venues. The Booking dataclass stores
information about a single booking, while the Venue class manages venue
information, availability slots, and provides thread-safe operations for
booking management.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import threading
import uuid
from typing import Dict, Any
from errors import ValidationError, SlotUnavailableError


@dataclass
class Booking:
    """
    Represents a single table booking at a venue.

    This dataclass stores all information related to a booking including
    the booking ID, venue details, time slot, number of people, user ID,
    and creation timestamp. Bookings are immutable once created.
    """

    booking_id: str  # Unique identifier for this booking
    venue_id: str  # ID of the venue where the booking is made
    slot: datetime  # Start time of the 1-hour booking slot
    num_people: int  # Number of people for the booking
    user_id: str  # ID of the user who made the booking
    created_at: datetime = field(
        default_factory=datetime.utcnow
    )  # When booking was created


class Venue:
    """
    Represents a venue (restaurant, hotel, etc.) with booking capabilities.

    This class manages venue information, availability slots, and provides
    thread-safe operations for booking management. It's designed to be
    generic enough to support different types of venues beyond restaurants.
    """

    def __init__(
        self, name: str, city: str, area: str, venue_type: str = "generic", **meta: Any
    ):
        """
        Initialize a new venue.

        Args:
            name: Name of the venue
            city: City where the venue is located
            area: Area/neighborhood within the city
            venue_type: Type of venue (e.g., "restaurant", "hotel")
            **meta: Additional metadata like cuisine, cost_for_two, is_veg, etc.
        """
        self.id: str = str(uuid.uuid4())  # Generate unique venue ID
        self.name = name
        self.city = city
        self.area = area
        self.venue_type = venue_type
        self.meta = meta  # Flexible metadata for venue-specific attributes

        # Availability management: maps time slot datetime to available tables
        self.availability: Dict[datetime, int] = {}

        # Thread safety locks
        self._lock = threading.RLock()  # Reentrant lock for venue-wide operations
        self._slot_locks: Dict[datetime, threading.Lock] = (
            {}
        )  # Per-slot locks for fine-grained concurrency

    def set_time_slot(self, slot_dt: datetime, tables: int):
        """
        Configure the number of available tables for a specific time slot.

        This method sets up a time slot with a specified number of available tables
        and creates a dedicated lock for this slot to ensure thread-safe bookings.

        Args:
            slot_dt: The datetime when the slot starts (1-hour duration)
            tables: Number of tables available for this slot

        Raises:
            ValidationError: If tables count is negative
        """
        if tables < 0:
            raise ValidationError("tables must be >= 0")
        with self._lock:
            self.availability[slot_dt] = tables
            # Create a dedicated lock for this slot if it doesn't exist
            if slot_dt not in self._slot_locks:
                self._slot_locks[slot_dt] = threading.Lock()

    def get_slot_lock(self, slot_dt: datetime) -> threading.Lock:
        """
        Get the thread-safe lock for a specific time slot.

        Each time slot has its own lock to allow concurrent bookings for
        different slots while preventing race conditions for the same slot.

        Args:
            slot_dt: The datetime of the slot to get the lock for

        Returns:
            threading.Lock: The lock object for the specified slot
        """
        with self._lock:
            # Create lock on-demand if it doesn't exist
            if slot_dt not in self._slot_locks:
                self._slot_locks[slot_dt] = threading.Lock()
            return self._slot_locks[slot_dt]

    def decrement_table_for_slot(self, slot_dt: datetime):
        """
        Atomically decrement the available tables count for a time slot.

        This method is called when a booking is confirmed and reduces the
        available table count by 1. It includes validation to ensure
        the slot exists and has available tables.

        Args:
            slot_dt: The datetime slot to decrement tables for

        Raises:
            SlotUnavailableError: If slot doesn't exist or no tables available
        """
        if slot_dt not in self.availability:
            raise SlotUnavailableError("Slot not registered")
        if self.availability[slot_dt] <= 0:
            raise SlotUnavailableError("No tables available")
        self.availability[slot_dt] -= 1

    def available_tables(self, slot_dt: datetime) -> int:
        """
        Get the number of available tables for a specific time slot.

        Args:
            slot_dt: The datetime slot to check availability for

        Returns:
            int: Number of available tables (0 if slot doesn't exist)
        """
        return self.availability.get(slot_dt, 0)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert venue information to a dictionary format.

        This method is useful for serialization, API responses, or
        displaying venue information in a structured format.

        Returns:
            Dict[str, Any]: Dictionary containing venue information and metadata
        """
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "area": self.area,
            "venue_type": self.venue_type,
            **self.meta,  # Include all metadata fields
        }
