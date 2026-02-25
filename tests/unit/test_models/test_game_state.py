"""Unit tests for GameState model."""

import pytest
from src.models.game_state import GameState, GameStatus
from src.models.snake import Snake
from src.models.food import Food
from src.models.position import Position
from src.models.direction import Direction


class TestGameStateCreation:
    """Test GameState creation and initialization."""

    def test_create_initial_state(self):
        """Test creating initial game state."""
        state = GameState.create_initial(width=20, height=20)

        assert isinstance(state.snake, Snake)
        assert isinstance(state.food, Food)
        assert state.score == 0
        assert state.status == GameStatus.PLAYING
        assert state.width == 20
        assert state.height == 20

    def test_create_custom_state(self):
        """Test creating custom game state."""
        snake = Snake.create_default()
        food = Food(position=Position(x=15, y=15))

        state = GameState(
            snake=snake,
            food=food,
            score=100,
            status=GameStatus.GAME_OVER,
            width=20,
            height=20
        )

        assert state.snake == snake
        assert state.food == food
        assert state.score == 100
        assert state.status == GameStatus.GAME_OVER


class TestGameStateUpdates:
    """Test GameState update methods."""

    def test_move_snake_without_eating(self):
        """Test moving snake without eating food."""
        state = GameState.create_initial(width=20, height=20)
        initial_length = len(state.snake)

        new_state = state.move_snake(grow=False)

        # Score unchanged
        assert new_state.score == state.score
        # Snake moved (length unchanged)
        assert len(new_state.snake) == initial_length
        # Food unchanged
        assert new_state.food == state.food

    def test_move_snake_with_eating(self):
        """Test moving snake and eating food."""
        # Create state where food is directly in front of snake
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        food = Food(position=Position(x=6, y=10))  # Right of snake head
        state = GameState(
            snake=snake,
            food=food,
            score=0,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        new_state = state.move_snake(grow=True)

        # Score increased
        assert new_state.score == 10
        # Snake grew
        assert len(new_state.snake) == len(state.snake) + 1

    def test_change_direction(self):
        """Test changing snake direction."""
        state = GameState.create_initial(width=20, height=20)
        initial_direction = state.snake.direction

        new_state = state.change_direction(Direction.UP)

        # Direction changed
        assert new_state.snake.direction == Direction.UP
        assert new_state.snake.direction != initial_direction

    def test_pause_toggle(self):
        """Test pausing and resuming game."""
        state = GameState.create_initial(width=20, height=20)

        # Pause
        paused_state = state.pause()
        assert paused_state.status == GameStatus.PAUSED

        # Resume
        resumed_state = paused_state.resume()
        assert resumed_state.status == GameStatus.PLAYING

    def test_game_over(self):
        """Test transitioning to game over state."""
        state = GameState.create_initial(width=20, height=20)

        game_over_state = state.game_over()

        assert game_over_state.status == GameStatus.GAME_OVER

    def test_respawn_food(self):
        """Test respawning food at new location."""
        snake = Snake.create_default()
        old_food = Food(position=Position(x=10, y=10))
        state = GameState(
            snake=snake,
            food=old_food,
            score=0,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        new_state = state.respawn_food()

        # New food at different location
        assert new_state.food != old_food
        # Food not on snake body
        assert not snake.contains(new_state.food.position)


class TestGameStatus:
    """Test GameStatus enum."""

    def test_status_values(self):
        """Test that all expected status values exist."""
        assert GameStatus.PLAYING is not None
        assert GameStatus.PAUSED is not None
        assert GameStatus.GAME_OVER is not None


class TestGameStateQuery:
    """Test GameState query methods."""

    def test_is_playing_true_when_playing(self):
        """Test is_playing returns True when playing."""
        state = GameState.create_initial(width=20, height=20)
        assert state.is_playing()

    def test_is_playing_false_when_paused(self):
        """Test is_playing returns False when paused."""
        state = GameState.create_initial(width=20, height=20).pause()
        assert not state.is_playing()

    def test_is_playing_false_when_game_over(self):
        """Test is_playing returns False when game over."""
        state = GameState.create_initial(width=20, height=20).game_over()
        assert not state.is_playing()

    def test_is_over_true_when_game_over(self):
        """Test is_over returns True when game over."""
        state = GameState.create_initial(width=20, height=20).game_over()
        assert state.is_over()
