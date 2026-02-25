"""Snake model for the Snake game."""

from dataclasses import dataclass
from typing import Tuple
from src.models.position import Position
from src.models.direction import Direction


@dataclass(frozen=True)
class Snake:
    """Represents the snake in the game.

    Attributes:
        body: Tuple of positions representing snake segments (head first).
        direction: Current movement direction.
    """

    body: Tuple[Position, ...]
    direction: Direction

    @property
    def head(self) -> Position:
        """Get the head position (first segment)."""
        return self.body[0]

    def __len__(self) -> int:
        """Get snake length (number of segments)."""
        return len(self.body)

    @property
    def body_positions(self) -> set:
        """Get body positions as a set for O(1) lookup."""
        return set(self.body)

    @classmethod
    def create_default(cls, width: int = 20, height: int = 20) -> "Snake":
        """Create a default snake with 3 horizontal segments.

        Args:
            width: Grid width for positioning (default 20).
            height: Grid height for positioning (default 20).

        Returns:
            A new Snake instance with default configuration.
        """
        # Position snake in the left-center of the grid
        start_y = height // 2
        start_x = width // 4

        body = (
            Position(x=start_x, y=start_y),
            Position(x=start_x - 1, y=start_y),
            Position(x=start_x - 2, y=start_y),
        )
        return cls(body=body, direction=Direction.RIGHT)

    def move(self, grow: bool = False) -> "Snake":
        """Move the snake forward in the current direction.

        Args:
            grow: If True, preserve tail (snake grows).
                  If False, remove tail (normal movement).

        Returns:
            A new Snake instance in the new position.
        """
        # Calculate new head position
        new_head = self.head + self.direction.delta

        # Build new body
        new_body = (new_head,) + self.body

        # Remove tail if not growing
        if not grow:
            new_body = new_body[:-1]

        return self.__class__(body=new_body, direction=self.direction)

    def grow(self) -> "Snake":
        """Grow the snake by adding a segment at the tail.

        Returns:
            A new Snake with an additional tail segment.
        """
        # Duplicate the tail segment to make the snake longer
        new_body = self.body + (self.body[-1],)
        return self.__class__(body=new_body, direction=self.direction)

    def change_direction(self, new_direction: Direction) -> "Snake":
        """Change the snake's direction.

        Args:
            new_direction: The new direction to face.

        Returns:
            A new Snake with updated direction (or same if invalid).

        Note:
            The snake cannot directly reverse (180° turn).
        """
        # Prevent 180° turns
        if self.direction.is_opposite(new_direction):
            return self

        return self.__class__(body=self.body, direction=new_direction)

    def collides_with_self(self) -> bool:
        """Check if the snake's head collides with its body.

        Returns:
            True if head position is in body (excluding head itself).
        """
        # Check if head appears more than once in body
        return self.body[1:].count(self.head) > 0

    def contains(self, position: Position) -> bool:
        """Check if the snake contains a given position.

        Args:
            position: The position to check.

        Returns:
            True if position is part of the snake's body.
        """
        return position in self.body_positions
