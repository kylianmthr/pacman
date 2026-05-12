# mypy: ignore-errors
import pygame
from pygame import mixer


class Music:
    def __init__(self, start_song, game_song, ghost_song, pacgum_song):
        mixer.init()
        self.start_song = start_song
        self.game_song = game_song
        self.ghost_song = ghost_song
        self.pacgum_song = pacgum_song

    def start_music(self):
        mixer.music.load(self.start_song)
        mixer.music.play()

    def pacgum_sound_effect(self):
        sound_effect = pygame.mixer.Sound(self.game_song)
        sound_effect.play()

    def superpacgum_sound_effect(self):
        sound_effect = pygame.mixer.Sound(self.pacgum_song)
        sound_effect.play()

    def ghost_sound_effect(self):
        mixer.music.load(self.ghost_song)
        mixer.music.play(loops=-1)
