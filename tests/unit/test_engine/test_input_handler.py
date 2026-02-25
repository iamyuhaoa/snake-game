"""Unit tests for InputHandler."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Use dummy driver for headless testing

import pygame
import pytest
from src.engine.input_handler import InputHandler, InputAction
from src.models.direction import Direction


class TestInputAction:
    """Test InputAction enum."""

    def test_all_actions_exist(self):
        """Test that all expected input actions exist."""
        assert InputAction.MOVE_UP is not None
        assert InputAction.MOVE_DOWN is not None
        assert InputAction.MOVE_LEFT is not None
        assert InputAction.MOVE_RIGHT is not None
        assert InputAction.PAUSE is not None
        assert InputAction.RESUME is not None
        assert InputAction.RESTART is not None
        assert InputAction.QUIT is not None


class TestInputHandler:
    """Test InputHandler key mapping."""

    def test_arrow_keys_map_to_directions(self):
        """Test arrow keys map to correct move actions."""
        handler = InputHandler()

        assert handler.handle_key(pygame.K_UP) == InputAction.MOVE_UP  # type: ignore
        assert handler.handle_key(pygame.K_DOWN) == InputAction.MOVE_DOWN  # type: ignore
        assert handler.handle_key(pygame.K_LEFT) == InputAction.MOVE_LEFT  # type: ignore
        assert handler.handle_key(pygame.K_RIGHT) == InputAction.MOVE_RIGHT  # type: ignore

    def test_wasd_keys_map_to_directions(self):
        """Test WASD keys map to correct move actions."""
        handler = InputHandler()

        assert handler.handle_key(pygame.K_w) == InputAction.MOVE_UP  # type: ignore
        assert handler.handle_key(pygame.K_s) == InputAction.MOVE_DOWN  # type: ignore
        assert handler.handle_key(pygame.K_a) == InputAction.MOVE_LEFT  # type: ignore
        assert handler.handle_key(pygame.K_d) == InputAction.MOVE_RIGHT  # type: ignore

    def test_space_key_toggles_pause(self):
        """Test space key maps to pause/resume."""
        handler = InputHandler()

        # Space key should return PAUSE action
        # The game loop handles toggle logic
        assert handler.handle_key(pygame.K_SPACE) == InputAction.PAUSE  # type: ignore

    def test_r_key_for_restart(self):
        """Test R key maps to restart action."""
        handler = InputHandler()

        assert handler.handle_key(pygame.K_r) == InputAction.RESTART  # type: ignore

    def test_q_and_esc_for_quit(self):
        """Test Q and ESC keys map to quit action."""
        handler = InputHandler()

        assert handler.handle_key(pygame.K_q) == InputAction.QUIT  # type: ignore
        assert handler.handle_key(pygame.K_ESCAPE) == InputAction.QUIT  # type: ignore

    def test_unknown_key_returns_none(self):
        """Test unknown keys return None."""
        handler = InputHandler()

        assert handler.handle_key(pygame.K_F1) is None  # type: ignore

    def test_action_to_direction_mapping(self):
        """Test converting input actions to directions."""
        assert InputAction.to_direction(InputAction.MOVE_UP) == Direction.UP
        assert InputAction.to_direction(InputAction.MOVE_DOWN) == Direction.DOWN
        assert InputAction.to_direction(InputAction.MOVE_LEFT) == Direction.LEFT
        assert InputAction.to_direction(InputAction.MOVE_RIGHT) == Direction.RIGHT

    def test_non_move_action_to_direction_returns_none(self):
        """Test non-move actions return None for direction."""
        assert InputAction.to_direction(InputAction.PAUSE) is None
        assert InputAction.to_direction(InputAction.QUIT) is None
        assert InputAction.to_direction(InputAction.RESTART) is None


# Note: Using real pygame since it's now installed
# We need to set up the display to avoid SDL errors
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Use dummy driver for headless testing
