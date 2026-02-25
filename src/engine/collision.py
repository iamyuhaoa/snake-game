"""Collision detection for the Snake game."""

from src.models.snake import Snake
from src.models.food import Food


class CollisionChecker:
    """Checks for game collisions."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize collision checker with grid dimensions.

        Args:
            width: Grid width (number of columns).
            height: Grid height (number of rows).
        """
        self.width = width
        self.height = height

    def check_wall_collision(self, snake: Snake) -> bool:
        """Check if snake's head is outside grid boundaries.

        Args:
            snake: The snake to check.

        Returns:
            True if snake head is out of bounds.
        """
        return not snake.head.is_in_bounds(self.width, self.height)

    def check_self_collision(self, snake: Snake) -> bool:
        """Check if snake's head collides with its body.

        Args:
            snake: The snake to check.

        Returns:
            True if snake head is in body (excluding head itself).
        """
        return snake.collides_with_self()

    def check_food_collision(self, snake: Snake, food: Food) -> bool:
        """Check if snake's head is on the food.

        Args:
            snake: The snake to check.
            food: The food to check.

        Returns:
            True if snake head position equals food position.
        """
        return snake.head == food.position

    def has_collision(self, snake: Snake, food: Food) -> bool:
        """Check if any game-ending collision exists.

        Args:
            snake: The snake to check.
            food: Current food position (to exclude food collision).

        Returns:
            True if wall or self collision exists.
        """
        return (
            self.check_wall_collision(snake)
            or self.check_self_collision(snake)
        )
