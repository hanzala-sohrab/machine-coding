"""
Demonstration scripts for the restaurant booking system.

This module contains demo functions that showcase the capabilities of the
booking system including concurrent booking handling, venue search functionality,
and error handling scenarios. These demos help illustrate the system's
thread-safe operations and feature set.
"""

from datetime import date, datetime, time, timedelta
import threading

from booking_system import BookingSystem
from models import Venue
from errors import BookingError


def iso_hour(dt: datetime) -> datetime:
    """
    Normalize a datetime to the start of the hour.

    This helper function removes minutes, seconds, and microseconds
    from a datetime object, creating a clean hourly time slot.

    Args:
        dt: The datetime to normalize

    Returns:
        datetime: The datetime normalized to the start of the hour
    """
    return dt.replace(minute=0, second=0, microsecond=0)


def demo_concurrent_booking():
    """
    Demonstrate concurrent booking capabilities and thread safety.

    This demo creates a restaurant with limited table availability and
    simulates multiple users trying to book the same time slot concurrently.
    It demonstrates:
    - Thread-safe booking operations
    - Proper lock handling to prevent double-booking
    - Graceful handling of failed booking attempts
    - Accurate tracking of successful vs failed bookings

    The demo shows that even with concurrent access, the system maintains
    data integrity and prevents overbooking.
    """
    print("=== Demo: concurrent booking ===")
    system = BookingSystem(booking_window_days=7)

    # Create a test restaurant with specific attributes
    r = Venue(
        name="Spice Heaven",
        city="Mumbai",
        area="Andheri",
        venue_type="restaurant",
        cuisine="Indian",
        is_veg=False,
        cost_for_two=800,
        total_tables=10,
    )
    rid = system.register_venue(r)

    # Set up a time slot for tomorrow at 8 PM with 5 available tables
    tomorrow = date.today() + timedelta(days=1)
    slot_dt = iso_hour(datetime.combine(tomorrow, time(hour=20)))
    system.update_time_slots(rid, [slot_dt], tables_each=2)

    results = []

    def try_book(user_no: int):
        """
        Attempt to book a table for a specific user.

        This function simulates a user trying to make a booking and
        records whether the attempt was successful or failed.

        Args:
            user_no: User number for identification
        """
        user_id = f"user_{user_no}"
        try:
            booking = system.book_table(
                user_id=user_id, venue_id=rid, slot_dt=slot_dt, num_people=4
            )
            print(f"[SUCCESS] {user_id} booked {booking.booking_id}")
            results.append((user_id, "success"))
        except BookingError as e:
            print(f"[FAILED ] {user_id} booking failed: {e}")
            results.append((user_id, "failed"))

    # Create and start 10 concurrent threads trying to book the same slot
    threads = [threading.Thread(target=try_book, args=(i + 1,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Display final results
    print("Final bookings:", len(system.list_bookings()))
    print("=== end demo ===\n")


def demo_search_and_errors():
    """
    Demonstrate venue search functionality and error handling.

    This demo showcases the advanced search capabilities of the system
    and demonstrates how various filters can be combined to find
    specific venues. It also shows proper error handling.

    The demo demonstrates:
    - Venue registration with different attributes
    - Search by city, cuisine, and dietary preferences
    - Filtering based on venue metadata
    - Proper display of search results
    """
    print("=== Demo: search and errors ===")
    system = BookingSystem(booking_window_days=2)

    # Create two different restaurants with varying attributes
    r1 = Venue(
        "Green Leaf",
        "Delhi",
        "Connaught",
        venue_type="restaurant",
        cuisine="Indian",
        is_veg=True,
        cost_for_two=500,
    )
    r2 = Venue(
        "Sea Grill",
        "Delhi",
        "Saket",
        venue_type="restaurant",
        cuisine="Seafood",
        is_veg=False,
        cost_for_two=1200,
    )
    system.register_venue(r1)
    system.register_venue(r2)

    # Demonstrate search functionality
    print("Veg restaurants in Delhi:")
    for v in system.search_venues(city="Delhi", veg_only=True):
        print(" -", v["name"])

    print("=== end demo ===\n")
