"""Game settings configuration."""

from dataclasses import dataclass


@dataclass
class Settings:
    """Game configuration settings."""

    # Grid dimensions
    GRID_WIDTH: int = 20
    GRID_HEIGHT: int = 20

    # Game speed (frames per second)
    FPS: int = 5  # Starting speed

    # Window size (in pixels)
    WINDOW_SIZE: int = 600

    # Points per food eaten
    POINTS_PER_FOOD: int = 10


# Default settings instance
DEFAULT_SETTINGS = Settings()
