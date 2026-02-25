"""Input handler for the Snake game."""

from enum import Enum
from typing import Optional
import pygame
from src.models.direction import Direction


class InputAction(Enum):
    """Input action enumeration."""

    MOVE_UP = "MOVE_UP"
    MOVE_DOWN = "MOVE_DOWN"
    MOVE_LEFT = "MOVE_LEFT"
    MOVE_RIGHT = "MOVE_RIGHT"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    RESTART = "RESTART"
    QUIT = "QUIT"

    @classmethod
    def to_direction(cls, action: "InputAction") -> Optional[Direction]:
        """Convert input action to direction.

        Args:
            action: The input action.

        Returns:
            Direction if action is a move action, None otherwise.
        """
        mapping = {
            cls.MOVE_UP: Direction.UP,
            cls.MOVE_DOWN: Direction.DOWN,
            cls.MOVE_LEFT: Direction.LEFT,
            cls.MOVE_RIGHT: Direction.RIGHT,
        }
        return mapping.get(action)


class InputHandler:
    """Maps keyboard input to game actions."""

    # Key to action mapping
    # Note: Use lowercase for letter keys as Pygame provides them that way
    KEY_MAP = {
        # Arrow keys
        pygame.K_UP: InputAction.MOVE_UP,
        pygame.K_DOWN: InputAction.MOVE_DOWN,
        pygame.K_LEFT: InputAction.MOVE_LEFT,
        pygame.K_RIGHT: InputAction.MOVE_RIGHT,
        # WASD keys
        pygame.K_w: InputAction.MOVE_UP,
        pygame.K_s: InputAction.MOVE_DOWN,
        pygame.K_a: InputAction.MOVE_LEFT,
        pygame.K_d: InputAction.MOVE_RIGHT,
        # Control keys
        pygame.K_SPACE: InputAction.PAUSE,
        pygame.K_r: InputAction.RESTART,
        pygame.K_q: InputAction.QUIT,
        pygame.K_ESCAPE: InputAction.QUIT,
    }

    def handle_key(self, key: int) -> Optional[InputAction]:
        """Handle a key press and return corresponding action.

        Args:
            key: Pygame key code.

        Returns:
            InputAction if key is mapped, None otherwise.
        """
        return self.KEY_MAP.get(key)
