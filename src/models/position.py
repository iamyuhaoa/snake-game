"""Position model for 2D grid coordinates."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Immutable 2D position on a grid.

    Attributes:
        x: The x-coordinate (column).
        y: The y-coordinate (row).
    """

    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        """Add two positions together.

        Args:
            other: Another position to add.

        Returns:
            A new Position with summed coordinates.
        """
        return Position(x=self.x + other.x, y=self.y + other.y)

    def is_adjacent(self, other: "Position") -> bool:
        """Check if another position is orthogonally adjacent.

        Args:
            other: Another position to check.

        Returns:
            True if positions are orthogonally adjacent (not diagonal).
        """
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def distance_to(self, other: "Position") -> int:
        """Calculate Manhattan distance to another position.

        Args:
            other: Another position.

        Returns:
            Manhattan distance (|dx| + |dy|).
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_in_bounds(self, width: int, height: int) -> bool:
        """Check if position is within grid boundaries.

        Args:
            width: Grid width (number of columns).
            height: Grid height (number of rows).

        Returns:
            True if 0 <= x < width and 0 <= y < height.
        """
        return 0 <= self.x < width and 0 <= self.y < height


# Class constant for origin
Position.ZERO = Position(x=0, y=0)
