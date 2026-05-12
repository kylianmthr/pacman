import pygame
from pygame import mixer


class Music:
    def __init__(
        self,
        start_song: str,
        game_song: str,
        ghost_song: str,
        pacgum_song: str,
    ) -> None:
        mixer.init()
        self.start_song = start_song
        self.game_song = game_song
        self.ghost_song = ghost_song
        self.pacgum_song = pacgum_song

    def start_music(self) -> None:
        mixer.music.load(self.start_song)
        mixer.music.play()

    def pacgum_sound_effect(self) -> None:
        sound_effect = pygame.mixer.Sound(self.game_song)
        sound_effect.play()

    def superpacgum_sound_effect(self) -> None:
        sound_effect = pygame.mixer.Sound(self.pacgum_song)
        sound_effect.play()

    def ghost_sound_effect(self) -> None:
        mixer.music.load(self.ghost_song)
        mixer.music.play(loops=-1)
