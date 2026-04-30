import pygame
from pygame.math import Vector2


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.name = text
        self.font = font
        self.image = self.font.render(text, True, color, None)
        self.rect = self.image.get_rect(center=coordinates)


class Text(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.name = text
        self.color = color
        self.font = font
        self.image = self.font.render(text, True, color, None)
        self.rect = self.image.get_rect(center=coordinates)


class Picture(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str,
        path: str,
        scale_width: int,
        scale_height: int,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(
            self.image, (scale_width, scale_height)
        )
        self.rect = self.image.get_rect(center=coordinates)


class WelcomeMenu:
    def __init__(self, screen, screen_width, screen_height):
        pygame.font.init()
        self.screen = screen
        self.assets = pygame.sprite.Group()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.button_idx = 0
        self.cursors_map = {}
        self.create_static_surfaces()

    def show_home_menu(self, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.assets.draw(self.screen)

    def stop_menu(self):
        for sprite in self.assets:
            sprite.kill()

    def update_sprite(
        self, sprite: pygame.sprite.Sprite, coordinates: tuple[int, int]
    ):
        sprite.rect = sprite.image.get_rect(center=coordinates)

    def update_cursor(self):
        for sprite in self.assets:
            if sprite.name == "right_selector":
                self.update_sprite(
                    sprite,
                    (
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "right"
                        ]
                    )
                    + Vector2(15, 0),
                )
            if sprite.name == "left_selector":
                self.update_sprite(
                    sprite,
                    (
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "left"
                        ]
                    )
                    + Vector2(-15, 0),
                )

    def item_selection(self, move: int):
        if len(self.buttons) > 0:
            self.button_idx = (self.button_idx + move) % len(self.buttons)
        self.update_cursor()

    def create_static_surfaces(self):
        pacfont = pygame.font.Font("./assets/PAC-FONT.TTF", 35)
        swfont = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        self.assets.add(
            Text(
                "1              9",
                "yellow",
                pacfont,
                (self.screen_width // 2, self.screen_height * 0.1),
            )
        )
        self.assets.add(
            Text(
                "PACMAN",
                "yellow",
                pacfont,
                (self.screen_width // 2, self.screen_height * 0.1),
            )
        )
        self.assets.add(
            Text(
                "22222222222222",
                "yellow",
                pacfont,
                (self.screen_width // 2, self.screen_height * 0.1 + 40),
            )
        )
        self.assets.add(
            Button(
                "START",
                "yellow",
                swfont,
                (self.screen_width // 2, self.screen_height * 0.5),
            )
        )
        self.assets.add(
            Button(
                "LEADERBOARD",
                "yellow",
                swfont,
                (self.screen_width // 2, self.screen_height * 0.5 + 50),
            )
        )
        self.assets.add(
            Button(
                "SETTINGS",
                "yellow",
                swfont,
                (self.screen_width // 2, self.screen_height * 0.5 + 100),
            )
        )
        self.buttons = [
            button for button in self.assets if isinstance(button, Button)
        ]
        self.cursors_map = {
            button.name: {
                "left": Vector2(button.rect.midleft),
                "right": Vector2(button.rect.midright),
            }
            for button in self.buttons
        }
        self.assets.add(
            Picture(
                "right_selector",
                "./assets/pacman_right.png",
                20,
                20,
                (
                    (
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "right"
                        ]
                    )
                    + Vector2(15, 0)
                ),
            )
        )
        self.assets.add(
            Picture(
                "left_selector",
                "./assets/pacman_left.png",
                20,
                20,
                (self.cursors_map[self.buttons[self.button_idx].name]["left"])
                + Vector2(-15, 0),
            )
        )


class Engine:
    def __init__(self, width=10, height=10) -> None:  # on set le min a 10*10 ?
        self.running = True
        self.frame_rate = 60
        self.screen_width = width * 40 + 10
        self.screen_height = height * 40 + 40
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.welcome_menu = WelcomeMenu(
            self.screen, self.screen_width, self.screen_height
        )

    def event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.welcome_menu.item_selection(-1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.welcome_menu.item_selection(+1)
            if event.type == pygame.QUIT:
                self.running = False

    def run(self) -> None:
        pygame.init()
        while self.running:
            self.event()
            self.screen.fill("black")
            self.welcome_menu.show_home_menu(
                self.screen_width, self.screen_height
            )
            self.clock.tick(self.frame_rate)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
