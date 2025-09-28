"""
Main entry point for the restaurant booking system demo.

This module serves as the entry point for running the restaurant booking
system demonstrations. It orchestrates the execution of various demo
functions that showcase the system's capabilities.
"""

from demo import demo_concurrent_booking, demo_search_and_errors


def main():
    """
    Main function that runs all booking system demonstrations.

    This function serves as the primary entry point for the demo application.
    It calls each demonstration function in sequence to showcase different
    aspects of the restaurant booking system:

    1. demo_concurrent_booking(): Shows thread-safe booking operations
       and demonstrates how the system handles concurrent booking attempts
       without allowing double-booking.

    2. demo_search_and_errors(): Demonstrates the venue search functionality
       with various filters and shows proper error handling.

    The main function provides a simple way to run all demos and see the
    complete functionality of the booking system in action.
    """
    # Run concurrent booking demo to show thread safety
    demo_concurrent_booking()

    # Run search and error handling demo
    demo_search_and_errors()


if __name__ == "__main__":
    """
    Standard Python entry point guard.

    This ensures that the main() function is only called when the script
    is executed directly (not when imported as a module). This is the
    recommended pattern for Python executable scripts.
    """
    main()
