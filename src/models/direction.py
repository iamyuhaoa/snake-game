"""Direction enum for snake movement."""

from enum import Enum
from src.models.position import Position


class Direction(Enum):
    """Cardinal directions for snake movement."""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    @property
    def delta(self) -> Position:
        """Get the position change for this direction."""
        deltas = {
            Direction.UP: Position(x=0, y=-1),
            Direction.DOWN: Position(x=0, y=1),
            Direction.LEFT: Position(x=-1, y=0),
            Direction.RIGHT: Position(x=1, y=0),
        }
        return deltas[self]

    @property
    def opposite(self) -> "Direction":
        """Get the opposite direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]

    def is_opposite(self, other: "Direction") -> bool:
        """Check if another direction is opposite to this one.

        Args:
            other: Another direction to compare.

        Returns:
            True if the directions are opposite.
        """
        return self.opposite == other

    @classmethod
    def all(cls) -> list["Direction"]:
        """Get all four cardinal directions.

        Returns:
            List of all directions.
        """
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
