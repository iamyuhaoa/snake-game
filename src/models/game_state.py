"""Game state model for the Snake game."""

from dataclasses import dataclass
from enum import Enum
from src.models.snake import Snake
from src.models.food import Food
from src.models.direction import Direction


class GameStatus(Enum):
    """Game status enumeration."""

    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


@dataclass(frozen=True)
class GameState:
    """Immutable game state.

    Attributes:
        snake: Current snake state.
        food: Current food position.
        score: Current score.
        status: Game status (playing, paused, game over).
        width: Grid width.
        height: Grid height.
    """

    snake: Snake
    food: Food
    score: int
    status: GameStatus
    width: int
    height: int

    @classmethod
    def create_initial(cls, width: int = 20, height: int = 20) -> "GameState":
        """Create initial game state.

        Args:
            width: Grid width.
            height: Grid height.

        Returns:
            A new GameState with default snake and random food.
        """
        snake = Snake.create_default(width, height)
        food = Food.spawn_random(width, height, forbidden=snake.body)
        return cls(
            snake=snake,
            food=food,
            score=0,
            status=GameStatus.PLAYING,
            width=width,
            height=height,
        )

    def move_snake(self, grow: bool = False) -> "GameState":
        """Move the snake and update state.

        Args:
            grow: If True, snake grows and score increases (ate food).
                  If False, normal move without scoring.

        Returns:
            A new GameState with updated snake and score.
        """
        new_snake = self.snake.move(grow=grow)
        new_score = self.score + 10 if grow else self.score
        return self.__class__(
            snake=new_snake,
            food=self.food,
            score=new_score,
            status=self.status,
            width=self.width,
            height=self.height,
        )

    def change_direction(self, direction: Direction) -> "GameState":
        """Change snake direction.

        Args:
            direction: New direction.

        Returns:
            A new GameState with updated direction.
        """
        new_snake = self.snake.change_direction(direction)
        return self.__class__(
            snake=new_snake,
            food=self.food,
            score=self.score,
            status=self.status,
            width=self.width,
            height=self.height,
        )

    def pause(self) -> "GameState":
        """Pause the game.

        Returns:
            A new GameState in PAUSED status.
        """
        return self.__class__(
            snake=self.snake,
            food=self.food,
            score=self.score,
            status=GameStatus.PAUSED,
            width=self.width,
            height=self.height,
        )

    def resume(self) -> "GameState":
        """Resume the game.

        Returns:
            A new GameState in PLAYING status.
        """
        return self.__class__(
            snake=self.snake,
            food=self.food,
            score=self.score,
            status=GameStatus.PLAYING,
            width=self.width,
            height=self.height,
        )

    def game_over(self) -> "GameState":
        """Transition to game over state.

        Returns:
            A new GameState in GAME_OVER status.
        """
        return self.__class__(
            snake=self.snake,
            food=self.food,
            score=self.score,
            status=GameStatus.GAME_OVER,
            width=self.width,
            height=self.height,
        )

    def with_score(self, score: int) -> "GameState":
        """Update score.

        Args:
            score: New score.

        Returns:
            A new GameState with updated score.
        """
        return self.__class__(
            snake=self.snake,
            food=self.food,
            score=score,
            status=self.status,
            width=self.width,
            height=self.height,
        )

    def respawn_food(self) -> "GameState":
        """Spawn food at new location avoiding snake body.

        Returns:
            A new GameState with new food position.
        """
        new_food = Food.spawn_random(
            self.width, self.height, forbidden=self.snake.body
        )
        return self.__class__(
            snake=self.snake,
            food=new_food,
            score=self.score,
            status=self.status,
            width=self.width,
            height=self.height,
        )

    def is_playing(self) -> bool:
        """Check if game is in playing state.

        Returns:
            True if status is PLAYING.
        """
        return self.status == GameStatus.PLAYING

    def is_over(self) -> bool:
        """Check if game is over.

        Returns:
            True if status is GAME_OVER.
        """
        return self.status == GameStatus.GAME_OVER
