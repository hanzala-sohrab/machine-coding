from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Callable
import threading
import uuid

from models import Venue, Booking
from errors import BookingError, NotFoundError, SlotUnavailableError, ValidationError


class BookingSystem:
    def __init__(self, booking_window_days: int = 30):
        self._venues: Dict[str, Venue] = {}
        self._bookings: Dict[str, Booking] = {}
        self._venues_lock = threading.RLock()
        self.booking_window_days = booking_window_days

    # ---------- Register / Update ----------
    def register_venue(self, venue: Venue) -> str:
        with self._venues_lock:
            self._venues[venue.id] = venue
        return venue.id

    def update_time_slots(
        self, venue_id: str, slot_dt_list: List[datetime], tables_each: int
    ):
        if tables_each < 0:
            raise ValidationError("tables_each must be >= 0")
        venue = self._get_venue_or_raise(venue_id)
        for slot_dt in slot_dt_list:
            if not self._is_within_booking_window(slot_dt.date()):
                raise ValidationError(f"Slot {slot_dt} is outside booking window")
        for slot_dt in slot_dt_list:
            venue.set_time_slot(slot_dt, tables_each)

    # ---------- Search ----------
    def search_venues(
        self,
        *,
        city: Optional[str] = None,
        area: Optional[str] = None,
        cuisine: Optional[str] = None,
        name: Optional[str] = None,
        cost_for_two_min: Optional[int] = None,
        cost_for_two_max: Optional[int] = None,
        veg_only: Optional[bool] = None,
        extra_filter: Optional[Callable[[Venue], bool]] = None,
    ) -> List[Dict[str, Any]]:
        results = []
        with self._venues_lock:
            for v in self._venues.values():
                if city and v.city.lower() != city.lower():
                    continue
                if area and v.area.lower() != area.lower():
                    continue
                if name and name.lower() not in v.name.lower():
                    continue
                if cuisine:
                    v_cuisine = v.meta.get("cuisine")
                    if not v_cuisine or cuisine.lower() not in str(v_cuisine).lower():
                        continue
                if veg_only is not None:
                    is_veg = v.meta.get("is_veg")
                    if veg_only and not is_veg:
                        continue
                cost = v.meta.get("cost_for_two")
                if cost is not None:
                    if cost_for_two_min and cost < cost_for_two_min:
                        continue
                    if cost_for_two_max and cost > cost_for_two_max:
                        continue
                if extra_filter and not extra_filter(v):
                    continue
                results.append(v.to_dict())
        return results

    # ---------- Book ----------
    def book_table(
        self, user_id: str, venue_id: str, slot_dt: datetime, num_people: int
    ) -> Booking:
        if num_people <= 0:
            raise ValidationError("num_people must be > 0")
        if not self._is_within_booking_window(slot_dt.date()):
            raise ValidationError("Booking beyond allowed window")

        venue = self._get_venue_or_raise(venue_id)
        slot_lock = venue.get_slot_lock(slot_dt)

        acquired = slot_lock.acquire(timeout=5)
        if not acquired:
            raise BookingError("Could not acquire lock, try again")

        try:
            available = venue.available_tables(slot_dt)
            if available <= 0:
                raise SlotUnavailableError("No tables available")

            venue.decrement_table_for_slot(slot_dt)

            booking = Booking(
                booking_id=str(uuid.uuid4()),
                venue_id=venue_id,
                slot=slot_dt,
                num_people=num_people,
                user_id=user_id,
            )
            with self._venues_lock:
                self._bookings[booking.booking_id] = booking
            return booking
        finally:
            slot_lock.release()

    # ---------- Helpers ----------
    def _get_venue_or_raise(self, venue_id: str) -> Venue:
        with self._venues_lock:
            v = self._venues.get(venue_id)
            if v is None:
                raise NotFoundError(f"Venue {venue_id} not found")
            return v

    def _is_within_booking_window(self, slot_date: date) -> bool:
        today = date.today()
        max_date = today + timedelta(days=self.booking_window_days)
        return today <= slot_date <= max_date

    def list_bookings(self) -> List[Booking]:
        with self._venues_lock:
            return list(self._bookings.values())
