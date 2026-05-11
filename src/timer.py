import pygame


class Timer:
    def __init__(self, duration: int):
        self.duration = duration * 1000
        self.current = pygame.time.get_ticks()

    def reset(self):
        self.current = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.current >= self.duration

    def current_time(self):
        return (pygame.time.get_ticks() - self.current) // 1000
