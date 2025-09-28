"""
Custom exception classes for the restaurant booking system.

This module defines a hierarchy of custom exceptions that are used throughout
the booking system to provide clear, specific error handling and meaningful
error messages to users and developers.
"""


class BookingError(Exception):
    """
    Base exception class for all booking-related errors.

    This is the root of the booking system exception hierarchy. All other
    booking-related exceptions inherit from this class, allowing for
    broad error catching and specific error handling.
    """

    pass


class NotFoundError(BookingError):
    """
    Exception raised when a requested resource is not found.

    This exception is used when a venue, booking, or other resource
    cannot be found in the system. It provides a clear indication that
    the requested entity does not exist.
    """

    pass


class SlotUnavailableError(BookingError):
    """
    Exception raised when a time slot is not available for booking.

    This exception is used in several scenarios:
    - The requested time slot has not been configured for the venue
    - The time slot exists but has no available tables remaining
    - The time slot is fully booked

    This helps users understand why their booking request was rejected.
    """

    pass


class ValidationError(BookingError):
    """
    Exception raised when input validation fails.

    This exception is used when user input or system parameters do not
    meet the required validation criteria. Examples include:
    - Negative number of people or tables
    - Booking dates outside the allowed window
    - Invalid venue configurations

    This provides clear feedback about what went wrong with the input.
    """

    pass
