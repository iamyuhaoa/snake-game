"""Unit tests for Direction model."""

import pytest
from src.models.direction import Direction
from src.models.position import Position


class TestDirectionEnum:
    """Test Direction enum values and properties."""

    def test_four_directions_exist(self):
        """Test that all four cardinal directions exist."""
        assert Direction.UP is not None
        assert Direction.DOWN is not None
        assert Direction.LEFT is not None
        assert Direction.RIGHT is not None

    def test_direction_has_delta(self):
        """Test that each direction has correct delta (dx, dy)."""
        assert Direction.UP.delta == Position(x=0, y=-1)
        assert Direction.DOWN.delta == Position(x=0, y=1)
        assert Direction.LEFT.delta == Position(x=-1, y=0)
        assert Direction.RIGHT.delta == Position(x=1, y=0)

    def test_direction_has_opposite(self):
        """Test that each direction has correct opposite."""
        assert Direction.UP.opposite == Direction.DOWN
        assert Direction.DOWN.opposite == Direction.UP
        assert Direction.LEFT.opposite == Direction.RIGHT
        assert Direction.RIGHT.opposite == Direction.LEFT


class TestDirectionOperations:
    """Test Direction utility methods."""

    def test_is_opposite(self):
        """Test checking if two directions are opposite."""
        assert Direction.UP.is_opposite(Direction.DOWN)
        assert Direction.DOWN.is_opposite(Direction.UP)
        assert Direction.LEFT.is_opposite(Direction.RIGHT)
        assert Direction.RIGHT.is_opposite(Direction.LEFT)

        # Not opposite
        assert not Direction.UP.is_opposite(Direction.LEFT)
        assert not Direction.UP.is_opposite(Direction.RIGHT)
        assert not Direction.DOWN.is_opposite(Direction.LEFT)

    def test_all_directions(self):
        """Test getting all directions as a list."""
        all_dirs = Direction.all()
        assert len(all_dirs) == 4
        assert Direction.UP in all_dirs
        assert Direction.DOWN in all_dirs
        assert Direction.LEFT in all_dirs
        assert Direction.RIGHT in all_dirs
