import pygame
from src.cheat import Cheats
from src.pacgum import Pacgum
from src.timer import Timer
from src.wall import Wall
from mazegen import generator
from pygame import mixer


class Game:
    def __init__(
        self,
        engine,
        screen,
        width,
        height,
        seed,
        points_per_pacgum,
        points_per_super_pacgum,
        points_per_ghost,
    ) -> None:
        from src.game_sprites import (
            Player,
            PinkGhost,
            RedGhost,
            BlueGhost,
            OrangeGhost,
            Ghost,
        )
        from src.hud import HUD

        self.engine = engine
        self.lives = 3
        self.timer = Timer(90)
        self.hud = HUD(self, self.engine)
        self.width = width
        self.height = height
        self.screen = screen
        self.sprites = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.player = Player(self, self.engine)
        self.player.rect.x = (self.width - 1) // 2 * 40 + 10
        self.player.rect.y = (self.height - 1) // 2 * 40 + 10
        self.maze = generator.MazeGenerator(
            self.width,
            self.height,
            seed,
            (0, 0),
            (self.width - 1, self.height - 1),
        )
        self.maze.generate((0, 0))
        self.maze.dig()
        ghosts: list[Ghost] = [
            RedGhost(self, (0, 6), (10, 10)),
            PinkGhost(self, (0, 8), ((self.width - 1) * 40 + 10, 10)),
            BlueGhost(
                self,
                (8, 8),
                ((self.width - 1) * 40 + 10, (self.height - 1) * 40 + 10),
            ),
            OrangeGhost(self, (0, 9), (10, (self.height - 1) * 40 + 10)),
        ]
        self.sprites.add(self.player)
        self.walls = pygame.sprite.Group()
        self.pacgums = pygame.sprite.Group()
        self.superpacgums = pygame.sprite.Group()
        for ghost in ghosts:
            self.ghosts.add(ghost)
            self.sprites.add(ghost)
        self.sprites.add(self.hud.score)
        self.sprites.add(self.hud.lives)
        self.sprites.add(self.hud.timer)
        self.create_walls()
        self.create_pacgums()
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.cheats = Cheats(self)

    def create_walls(self) -> None:
        offset_y = 0
        for row in self.maze.maze:
            offset_x = 0
            for col in row:
                walls = []
                if int(col[3]):
                    walls += [Wall(50, 10, (0 + offset_x, 0 + offset_y))]
                if int(col[0]):
                    walls += [Wall(10, 50, (0 + offset_x, 0 + offset_y))]
                if col == "1111":
                    walls += [
                        Wall(30, 30, (10 + offset_x, 10 + offset_y), "blue")
                    ]
                self.walls.add(walls)
                self.sprites.add(walls)
                offset_x += 40
            offset_y += 40
        bottom_wall = Wall(40 * self.width + 10, 10, (0, offset_y))
        self.walls.add(bottom_wall)
        self.sprites.add(bottom_wall)
        right_wall = Wall(10, 40 * self.height + 10, (40 * self.width, 0))
        self.walls.add(right_wall)
        self.sprites.add(right_wall)

    def get_superpacgum(self) -> list[tuple[int, int]]:
        return [
            (0, 0),
            (self.width - 1, 0),
            (self.width - 1, self.height - 1),
            (0, self.height - 1),
        ]

    def create_pacgums(self) -> None:
        offset_y = 23
        y = 0
        superpacugums = self.get_superpacgum()
        for row in self.maze.maze:
            x = 0
            offset_x = 23
            for col in row:
                if col != "1111":
                    if (x, y) in superpacugums:
                        pacgum = Pacgum(5, (offset_x, offset_y))
                        self.superpacgums.add(pacgum)
                        self.sprites.add(pacgum)
                    else:
                        pacgum = Pacgum(2, (offset_x, offset_y))
                        self.pacgums.add(pacgum)
                        self.sprites.add(pacgum)
                x += 1
                offset_x += 40
            y += 1
            offset_y += 40

    def respawn(self) -> None:
        self.lives -= 1
        self.player.rect.x = (self.width - 1) // 2 * 40 + 10
        self.player.rect.y = (self.height - 1) // 2 * 40 + 10
        coords = [
            (10, 10),
            ((self.width - 1) * 40 + 10, 10),
            ((self.width - 1) * 40 + 10, (self.height - 1) * 40 + 10),
            (10, (self.height - 1) * 40 + 10),
        ]
        for i in range(len(self.ghosts.sprites())):
            current_time = pygame.time.get_ticks()
            self.ghosts.sprites()[i].rect.x = coords[i][0]
            self.ghosts.sprites()[i].rect.y = coords[i][1]
            self.ghosts.sprites()[i].eaten = False
            self.ghosts.sprites()[i].evade = False
            self.ghosts.sprites()[i].last_cycle = current_time
            self.ghosts.sprites()[i].images = []
            self.ghosts.sprites()[i].set_animation()
            self.ghosts.sprites()[i].direction = self.ghosts.sprites()[
                i
            ].target_player(self.player.get_coordinates())

    def event(self, event) -> None:
        from src.game_sprites import Direction

        self.cheats.event(event)

        if event.type == pygame.KEYDOWN:
            player = self.sprites.sprites()[0]
            if event.key == pygame.K_LEFT:
                player.disered_direction = Direction.WEST
            if event.key == pygame.K_DOWN:
                player.disered_direction = Direction.SOUTH
            if event.key == pygame.K_UP:
                player.disered_direction = Direction.NORTH
            if event.key == pygame.K_RIGHT:
                player.disered_direction = Direction.EAST

    def update(self) -> None:
        self.sprites.update()
        self.screen.fill("black")
        self.sprites.draw(self.screen)
        if len(self.pacgums.sprites()) == 0 and not self.engine.loading:
            self.engine.loading = True
            self.engine.next_level()
        if self.lives < 0 or self.timer.is_expired():
            self.engine.menu_active = True
            self.engine.menu.switch_menu("game_over_menu")
            mixer.music.stop()
