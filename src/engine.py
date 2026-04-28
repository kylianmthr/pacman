import pygame


class Engine:
    def __init__(self) -> None:
        self.running = True
        self.frame_rate = 60
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        pygame.init()
        while self.running:
            self.clock.tick(self.frame_rate)
        pygame.quit()
