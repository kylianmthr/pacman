"""Audio helper for background music and sound effects."""

import pygame
from pygame import mixer


class Music:
    """Manage music and sound effects playback."""

    def __init__(
        self,
        start_song: str,
        game_song: str,
        ghost_song: str,
        pacgum_song: str,
    ) -> None:
        """Initialize the audio system and track file paths.

        Args:
            start_song: Path to the start music track.
            game_song: Path to the pacgum sound effect (legacy name retained).
            ghost_song: Path to the ghost chase music track.
            pacgum_song: Path to the super pacgum sound effect.
        """
        mixer.init()
        self.start_song = start_song
        self.game_song = game_song
        self.ghost_song = ghost_song
        self.pacgum_song = pacgum_song

    def start_music(self) -> None:
        """Play the start music once."""
        mixer.music.load(self.start_song)
        mixer.music.play()

    def pacgum_sound_effect(self) -> None:
        """Play the pacgum sound effect."""
        sound_effect = pygame.mixer.Sound(self.game_song)
        sound_effect.play()

    def superpacgum_sound_effect(self) -> None:
        """Play the super pacgum sound effect."""
        sound_effect = pygame.mixer.Sound(self.pacgum_song)
        sound_effect.play()

    def ghost_sound_effect(self) -> None:
        """Loop the ghost chase music track."""
        mixer.music.load(self.ghost_song)
        mixer.music.play(loops=-1)
