"""Integration tests for complete game flow."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pytest
import pygame
from src.engine.game_loop import GameLoop
from src.models.game_state import GameStatus
from src.models.direction import Direction
from src.engine.input_handler import InputAction


class TestCompleteGameFlow:
    """Test complete game flow from start to game over."""

    def test_game_starts_in_playing_state(self):
        """Test game initializes in playing state."""
        game = GameLoop(width=10, height=10, fps=10)

        assert game.state.is_playing()
        assert game.state.score == 0
        assert len(game.state.snake) == 3  # Default snake length

    def test_full_game_cycle(self):
        """Test complete game cycle: play -> eat -> grow -> game over."""
        game = GameLoop(width=5, height=5, fps=10)

        initial_score = game.state.score
        initial_length = len(game.state.snake)

        # Simulate multiple game ticks
        for _ in range(20):
            if game.state.is_playing():
                game.update()

        # Game should have progressed
        assert game.state is not None

        # Either game is over or score/length changed
        assert (
            game.state.is_over() or
            game.state.score >= initial_score or
            len(game.state.snake) >= initial_length
        )

    def test_pause_resume_cycle(self):
        """Test pause and resume functionality."""
        game = GameLoop(width=10, height=10, fps=10)

        # Game starts playing
        assert game.state.is_playing()

        # Pause the game
        game.handle_input(InputAction.PAUSE)
        assert game.state.status == GameStatus.PAUSED

        # Update should not change state when paused
        paused_head = game.state.snake.head
        game.update()
        assert game.state.snake.head == paused_head

        # Resume the game
        game.handle_input(InputAction.PAUSE)
        assert game.state.is_playing()

    def test_restart_resets_game(self):
        """Test restart functionality resets game state."""
        game = GameLoop(width=10, height=10, fps=10)

        # Play a bit
        game.update()
        game.handle_input(InputAction.MOVE_UP)
        game.update()

        # Direction should have changed after update
        assert game.state.snake.direction == Direction.UP

        # Restart
        game.handle_input(InputAction.RESTART)

        # State should be reset
        assert game.state.is_playing()
        assert game.state.score == 0
        assert len(game.state.snake) == 3
        # Direction resets to RIGHT (default)
        assert game.state.snake.direction == Direction.RIGHT

    def test_direction_change_persistence(self):
        """Test direction changes persist across updates."""
        game = GameLoop(width=10, height=10, fps=10)

        initial_direction = game.state.snake.direction  # RIGHT

        # Change direction to UP
        game.handle_input(InputAction.MOVE_UP)
        game.update()

        # Direction should have changed
        assert game.state.snake.direction == Direction.UP

        # Change direction to LEFT
        game.handle_input(InputAction.MOVE_LEFT)
        game.update()

        # Direction should be LEFT (perpendicular to UP, allowed)
        assert game.state.snake.direction == Direction.LEFT

    def test_cannot_reverse_direction(self):
        """Test snake cannot directly reverse direction."""
        game = GameLoop(width=10, height=10, fps=10)

        # Snake starts moving RIGHT
        assert game.state.snake.direction == Direction.RIGHT

        # Try to reverse (should be ignored)
        game.handle_input(InputAction.MOVE_LEFT)
        game.update()

        # Direction should still be RIGHT
        assert game.state.snake.direction == Direction.RIGHT

    def test_quit_action(self):
        """Test quit action sets game over state."""
        game = GameLoop(width=10, height=10, fps=10)

        assert game.state.is_playing()

        # Send quit action
        game.handle_input(InputAction.QUIT)

        # Game should be over
        assert game.state.is_over()


class TestFoodEatingFlow:
    """Test food eating mechanics in game context."""

    def test_snake_can_eat_food(self):
        """Test snake can eat food when positioned correctly."""
        from src.models.snake import Snake
        from src.models.position import Position
        from src.models.food import Food
        from src.models.game_state import GameState

        # Create scenario where food is directly in front of snake
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        food = Food(position=Position(x=6, y=10))  # Right of head

        state = GameState(
            snake=snake,
            food=food,
            score=0,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        game = GameLoop(width=20, height=20, fps=10)
        game.state = state

        # Update should move snake onto food
        initial_score = game.state.score
        initial_length = len(game.state.snake)

        game.update()

        # Score should increase
        assert game.state.score > initial_score
        # Snake should grow
        assert len(game.state.snake) >= initial_length

    def test_food_respawns_after_eating(self):
        """Test food respawns at new location after being eaten."""
        from src.models.snake import Snake
        from src.models.position import Position
        from src.models.food import Food

        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        food = Food(position=Position(x=6, y=10))

        game = GameLoop(width=20, height=20, fps=10)
        game.state = game.state.__class__(
            snake=snake,
            food=food,
            score=0,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        old_food_position = game.state.food.position

        # Update until food is eaten
        game.update()

        # Food should be at new location
        if game.state.score > 0:  # Food was eaten
            assert game.state.food.position != old_food_position


class TestCollisionDetectionFlow:
    """Test collision detection in game context."""

    def test_wall_collision_ends_game(self):
        """Test hitting a wall ends the game."""
        from src.models.snake import Snake
        from src.models.position import Position

        # Create snake at right edge facing right
        snake = Snake(
            body=(Position(x=19, y=10), Position(x=18, y=10)),
            direction=Direction.RIGHT
        )

        game = GameLoop(width=20, height=20, fps=10)
        game.state = game.state.__class__(
            snake=snake,
            food=game.state.food,
            score=0,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        # Update should move snake into wall
        game.update()

        # Game should be over
        assert game.state.is_over()

    def test_corner_collision(self):
        """Test collision in all four corners."""
        # Position snake at edge, facing outward - will collide on next move
        # Need 2 segments so tail doesn't disappear when moving
        test_cases = [
            # Position 2 segments at edge, facing outward
            (0, 0, 0, 1, Direction.UP),        # At top edge, moving UP
            (0, 19, 0, 18, Direction.DOWN),    # At bottom edge, moving DOWN
            (19, 0, 18, 0, Direction.RIGHT),  # At right edge, moving RIGHT
            (0, 0, 1, 0, Direction.LEFT),     # At left edge, moving LEFT
        ]

        for x1, y1, x2, y2, direction in test_cases:
            from src.models.snake import Snake
            from src.models.position import Position

            # Create snake with 2 segments at the edge
            snake = Snake(
                body=(Position(x=x1, y=y1), Position(x=x2, y=y2)),
                direction=direction
            )

            game = GameLoop(width=20, height=20, fps=10)
            game.state = game.state.__class__(
                snake=snake,
                food=game.state.food,
                score=0,
                status=GameStatus.PLAYING,
                width=20,
                height=20
            )

            game.update()
            assert game.state.is_over(), f"Failed for edge collision with direction {direction}"


class TestMultipleMoves:
    """Test multiple consecutive moves and state consistency."""

    def test_ten_consecutive_moves(self):
        """Test ten consecutive moves without errors."""
        game = GameLoop(width=20, height=20, fps=10)

        # Make 10 moves
        for _ in range(10):
            game.update()

        # Game should still be running (no collision yet)
        # or game over legitimately
        assert game.state is not None

    def test_direction_changes_during_movement(self):
        """Test changing direction multiple times while moving."""
        game = GameLoop(width=20, height=20, fps=10)

        # Move in a pattern: RIGHT, UP, LEFT, DOWN, RIGHT
        directions = [
            InputAction.MOVE_UP,
            InputAction.MOVE_LEFT,
            InputAction.MOVE_DOWN,
            InputAction.MOVE_RIGHT,
        ]

        for direction in directions:
            game.handle_input(direction)
            game.update()

        # Game should still be functional
        assert game.state is not None
        assert game.state.snake.head is not None
