import pygame


class Cheats:
    def __init__(self, game):
        self.game = game
        self.invisibility = False
        self.speed = 1

    def event(self, evt) -> None:
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_i:
                self.invisibility = not self.invisibility
            elif evt.key == pygame.K_s:
                if self.speed == 1:
                    self.speed = 2
                else:
                    self.speed = 1
            elif evt.key == pygame.K_l:
                self.game.engine.next_level()
            elif evt.key == pygame.K_e:
                self.game.lives += 1
