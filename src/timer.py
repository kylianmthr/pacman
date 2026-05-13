"""Utility timer for level time tracking."""

import pygame


class Timer:
    """Track elapsed time with pause support."""

    def __init__(self, duration: int):
        """Initialize the timer with a duration in seconds.

        Args:
            duration: Duration in seconds for the timer.
        """
        self.duration = duration * 1000
        self.start_ticks = pygame.time.get_ticks()
        self.accumulated_time = 0
        self.paused = False

    def toggle_pause(self) -> None:
        """Toggle the paused state while preserving elapsed time."""
        if not self.paused:
            self.accumulated_time += pygame.time.get_ticks() - self.start_ticks
            self.paused = True
        else:
            self.start_ticks = pygame.time.get_ticks()
            self.paused = False

    def reset(self) -> None:
        """Reset the timer to its initial state."""
        self.start_ticks = pygame.time.get_ticks()
        self.accumulated_time = 0
        self.paused = False

    def get_elapsed_time(self) -> int:
        """Return the elapsed time in milliseconds.

        Returns:
            Elapsed time in milliseconds.
        """
        if self.paused:
            return self.accumulated_time
        return self.accumulated_time + (
            pygame.time.get_ticks() - self.start_ticks
        )

    def is_expired(self) -> bool:
        """Check whether the timer has expired.

        Returns:
            True if elapsed time exceeds the duration.
        """
        return self.get_elapsed_time() >= self.duration

    def current_time(self) -> int:
        """Return the remaining time in seconds.

        Returns:
            Remaining time in seconds.
        """
        return self.duration // 1000 - self.get_elapsed_time() // 1000
