"""Food model for the Snake game."""

import random
from dataclasses import dataclass
from typing import Iterable, Optional
from src.models.position import Position


@dataclass(frozen=True)
class Food:
    """Represents food on the game board.

    Attributes:
        position: The position where food is located.
    """

    position: Position

    @classmethod
    def spawn_random(
        cls,
        width: int,
        height: int,
        forbidden: Optional[Iterable[Position]] = None,
    ) -> "Food":
        """Spawn food at a random position avoiding forbidden locations.

        Args:
            width: Grid width.
            height: Grid height.
            forbidden: Positions where food cannot spawn (e.g., snake body).

        Returns:
            A new Food instance at a valid random position.

        Raises:
            ValueError: If no valid position exists.
        """
        forbidden_set = set(forbidden) if forbidden else set()

        # Generate all possible positions
        all_positions = {
            Position(x=x, y=y)
            for x in range(width)
            for y in range(height)
        }

        # Remove forbidden positions
        valid_positions = all_positions - forbidden_set

        if not valid_positions:
            raise ValueError("No valid position to spawn food")

        # Select random position
        position = random.choice(list(valid_positions))
        return cls(position=position)
