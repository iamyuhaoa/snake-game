"""Color configuration for the Snake game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    """Game color scheme."""

    # Background colors
    BACKGROUND: tuple = (20, 20, 30)  # Dark blue-gray
    GRID: tuple = (30, 30, 45)  # Slightly lighter for grid lines

    # Snake colors
    SNAKE_HEAD: tuple = (76, 175, 80)  # Green
    SNAKE_BODY: tuple = (56, 142, 60)  # Darker green
    SNAKE_BORDER: tuple = (27, 94, 32)  # Very dark green

    # Food color
    FOOD: tuple = (244, 67, 54)  # Red

    # Text colors
    TEXT_PRIMARY: tuple = (255, 255, 255)  # White
    TEXT_SECONDARY: tuple = (200, 200, 200)  # Light gray

    # UI colors
    SCORE_BACKGROUND: tuple = (0, 0, 0, 128)  # Semi-transparent black


# Default color scheme
DEFAULT_COLORS = Colors()
