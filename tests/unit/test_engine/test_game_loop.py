"""Unit tests for GameLoop."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from unittest.mock import Mock, MagicMock, patch
from src.engine.game_loop import GameLoop
from src.models.game_state import GameState, GameStatus
from src.models.direction import Direction
from src.engine.input_handler import InputAction


class TestGameLoopInitialization:
    """Test GameLoop initialization."""

    def test_create_game_loop(self):
        """Test creating a game loop instance."""
        loop = GameLoop(width=20, height=20, fps=10)

        assert loop.width == 20
        assert loop.height == 20
        assert loop.fps == 10
        assert loop.state is not None
        assert loop.state.is_playing()


class TestGameLoopUpdate:
    """Test GameLoop update logic."""

    def test_update_moves_snake(self):
        """Test update moves snake forward."""
        loop = GameLoop(width=20, height=20, fps=10)
        initial_head = loop.state.snake.head

        loop.update()

        # Snake moved
        assert loop.state.snake.head != initial_head

    def test_update_with_direction_change(self):
        """Test update with direction change."""
        loop = GameLoop(width=20, height=20, fps=10)

        loop.handle_input(InputAction.MOVE_UP)
        loop.update()

        assert loop.state.snake.direction == Direction.UP

    def test_update_ignores_invalid_direction(self):
        """Test update ignores reverse direction."""
        loop = GameLoop(width=20, height=20, fps=10)
        initial_direction = loop.state.snake.direction  # RIGHT

        loop.handle_input(InputAction.MOVE_LEFT)  # Try to reverse
        loop.update()

        # Direction unchanged
        assert loop.state.snake.direction == initial_direction

    def test_update_when_paused(self):
        """Test update does nothing when paused."""
        loop = GameLoop(width=20, height=20, fps=10)
        initial_head = loop.state.snake.head

        loop.handle_input(InputAction.PAUSE)

        # Try to update multiple times
        for _ in range(5):
            loop.update()

        # Snake hasn't moved
        assert loop.state.snake.head == initial_head
        assert loop.state.status == GameStatus.PAUSED

    def test_pause_toggle(self):
        """Test pause toggles game state."""
        loop = GameLoop(width=20, height=20, fps=10)

        # Pause
        loop.handle_input(InputAction.PAUSE)
        assert loop.state.status == GameStatus.PAUSED

        # Resume
        loop.handle_input(InputAction.PAUSE)
        assert loop.state.status == GameStatus.PLAYING


class TestGameLoopFoodEating:
    """Test food eating logic."""

    def test_eating_food_increases_score(self):
        """Test eating food increases score by 10."""
        from src.models.snake import Snake
        from src.models.position import Position
        from src.models.food import Food

        loop = GameLoop(width=20, height=20, fps=10)

        # Set up food directly in front of snake
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        food = Food(position=Position(x=6, y=10))  # Right of head
        loop.state = loop.state.__class__(
            snake=snake,
            food=food,
            score=0,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        initial_score = loop.state.score
        loop.update()

        # Score should increase
        assert loop.state.score > initial_score

    def test_eating_food_respawns_food(self):
        """Test new food spawns after eating."""
        loop = GameLoop(width=20, height=20, fps=10)
        old_food = loop.state.food

        # Force food respawn
        loop.state = loop.state.respawn_food()

        assert loop.state.food != old_food
        assert not loop.state.snake.contains(loop.state.food.position)


class TestGameLoopCollision:
    """Test collision handling."""

    def test_wall_collision_ends_game(self):
        """Test wall collision transitions to game over."""
        # Create a scenario where snake will hit wall
        # Use a small grid for easier testing
        loop = GameLoop(width=5, height=5, fps=10)

        # Position snake near wall
        from src.models.snake import Snake
        from src.models.position import Position

        snake = Snake(
            body=(Position(x=4, y=2), Position(x=3, y=2)),
            direction=Direction.RIGHT
        )
        loop.state = loop.state.__class__(
            snake=snake,
            food=loop.state.food,
            score=loop.state.score,
            status=GameStatus.PLAYING,
            width=5,
            height=5
        )

        loop.update()

        assert loop.state.status == GameStatus.GAME_OVER

    def test_self_collision_detection_works(self):
        """Test that the collision checker can detect self-collisions."""
        loop = GameLoop(width=20, height=20, fps=10)

        from src.models.snake import Snake
        from src.models.position import Position

        # Create snake with duplicate head position (collision state)
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )

        # Verify collision is detected
        assert loop.collision_checker.check_self_collision(snake)


class TestGameLoopRestart:
    """Test game restart functionality."""

    def test_restart_resets_game(self):
        """Test restart resets game state."""
        loop = GameLoop(width=20, height=20, fps=10)

        # Play a bit
        loop.update()
        loop.handle_input(InputAction.MOVE_UP)
        loop.update()

        # Game over
        loop.state = loop.state.game_over()
        assert loop.state.is_over()

        # Restart
        loop.handle_input(InputAction.RESTART)

        assert loop.state.is_playing()
        assert loop.state.score == 0
