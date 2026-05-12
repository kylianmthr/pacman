import pygame


class Timer:
    def __init__(self, duration: int):
        self.duration = duration * 1000
        self.start_ticks = pygame.time.get_ticks()
        self.accumulated_time = 0
        self.paused = False

    def toggle_pause(self):
        if not self.paused:
            self.accumulated_time += pygame.time.get_ticks() - self.start_ticks
            self.paused = True
        else:
            self.start_ticks = pygame.time.get_ticks()
            self.paused = False

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()
        self.accumulated_time = 0
        self.paused = False

    def get_elapsed_time(self):
        if self.paused:
            return self.accumulated_time
        return self.accumulated_time + (
            pygame.time.get_ticks() - self.start_ticks
        )

    def is_expired(self):
        return self.get_elapsed_time() >= self.duration

    def current_time(self):
        return self.get_elapsed_time() // 1000
