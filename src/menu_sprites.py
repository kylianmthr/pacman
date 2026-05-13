"""Sprite helpers for menu UI elements."""

import pygame
from pygame.surface import Surface


class Button(pygame.sprite.Sprite):
    """Clickable or selectable menu button."""

    def __init__(
        self,
        name: str,
        object: pygame.font.Font | str,
        coordinates: tuple[int, int],
        position: int,
        color: str,
        scale_width: int = 40,
        scale_height: int = 40,
    ) -> None:
        """Initialize a button from text or an image.

        Args:
            name: Button identifier or text.
            object: Font for text rendering or image path.
            coordinates: Center coordinates for the button.
            position: Ordering index used for cursor navigation.
            color: Text color for font rendering.
            scale_width: Target width when using image assets.
            scale_height: Target height when using image assets.
        """
        super().__init__()
        self.name = name
        self.object = object
        self.position = position
        self.coordinates = coordinates
        self.color = color
        self.scale_width = scale_width
        self.scale_height = scale_height
        self.image: Surface = self.choose_type()
        self.rect = self.image.get_rect(center=coordinates)

    def choose_type(self) -> Surface:
        """Render the button text or load the image surface.

        Returns:
            Rendered surface for the button.
        """
        if isinstance(self.object, pygame.font.Font):
            return self.object.render(self.name, True, self.color, None)
        image = pygame.image.load(self.object)
        return pygame.transform.smoothscale(
            image, (self.scale_width, self.scale_height)
        )


class Text(pygame.sprite.Sprite):
    """Simple centered text sprite."""

    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ) -> None:
        """Create a text sprite centered at the given coordinates.

        Args:
            text: Text content to render.
            color: Text color.
            font: Font used for rendering.
            coordinates: Center coordinates for the text.
        """
        super().__init__()
        self.coordinates = coordinates
        self.name = text
        self.color = color
        self.font = font
        self.text = text
        self.image = self.font.render(self.text, True, color, None)
        self.rect = self.image.get_rect(center=coordinates)


class TextFromRight(pygame.sprite.Sprite):
    """Text sprite aligned from the right edge."""

    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ) -> None:
        """Create a text sprite aligned to the right.

        Args:
            text: Text content to render.
            color: Text color.
            font: Font used for rendering.
            coordinates: Right-aligned coordinates.
        """
        super().__init__()
        self.name = text
        self.color = color
        self.font = font
        self.image = self.font.render(text, True, color, None)
        self.rect = self.image.get_rect(midright=coordinates)


class TextFromLeft(pygame.sprite.Sprite):
    """Text sprite aligned from the left edge."""

    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ) -> None:
        """Create a text sprite aligned to the left.

        Args:
            text: Text content to render.
            color: Text color.
            font: Font used for rendering.
            coordinates: Left-aligned coordinates.
        """
        super().__init__()
        self.name = text
        self.text = text
        self.color = color
        self.font = font
        self.image = self.font.render(self.text, True, color, None)
        self.rect = self.image.get_rect(midleft=coordinates)

    def get_size(self) -> tuple[int, int]:
        """Return the rendered text dimensions.

        Returns:
            Width and height of the rendered text.
        """
        return self.font.size(self.text)


class Picture(pygame.sprite.Sprite):
    """Image sprite scaled to a target size."""

    def __init__(
        self,
        name: str,
        path: str,
        scale_width: int,
        scale_height: int,
        coordinates: tuple[int, int],
    ):
        """Load and scale an image sprite.

        Args:
            name: Identifier for the sprite.
            path: Path to the image file.
            scale_width: Target width in pixels.
            scale_height: Target height in pixels.
            coordinates: Center coordinates for placement.
        """
        super().__init__()
        self.name = name
        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(
            self.image, (scale_width, scale_height)
        )
        self.rect = self.image.get_rect(center=coordinates)


class Box(pygame.sprite.Sprite):
    """Semi-transparent rectangle used for overlays."""

    def __init__(
        self,
        width: int,
        height: int,
        coordinates: tuple[int, int],
        alpha: int = 100,
        color: str = "black",
        name: str = "box",
    ) -> None:
        """Create a colored rectangle surface.

        Args:
            width: Width of the box in pixels.
            height: Height of the box in pixels.
            coordinates: Center coordinates for placement.
            alpha: Alpha transparency value.
            color: Fill color.
            name: Sprite identifier.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect(center=coordinates)
        self.name = name
