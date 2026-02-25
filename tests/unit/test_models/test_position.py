"""Unit tests for Position model."""

import pytest
from src.models.position import Position


class TestPositionCreation:
    """Test Position model creation and initialization."""

    def test_create_position_with_valid_coordinates(self):
        """Test creating a position with valid x and y coordinates."""
        position = Position(x=5, y=10)
        assert position.x == 5
        assert position.y == 10

    def test_position_is_immutable(self):
        """Test that Position is immutable (frozen dataclass)."""
        position = Position(x=5, y=10)
        with pytest.raises(AttributeError):
            position.x = 10  # type: ignore


class TestPositionEquality:
    """Test Position equality and comparison."""

    def test_equal_positions(self):
        """Test that two positions with same coordinates are equal."""
        pos1 = Position(x=5, y=10)
        pos2 = Position(x=5, y=10)
        assert pos1 == pos2

    def test_unequal_positions(self):
        """Test that positions with different coordinates are not equal."""
        pos1 = Position(x=5, y=10)
        pos2 = Position(x=6, y=10)
        assert pos1 != pos2

    def test_position_hashable(self):
        """Test that Position is hashable (can be used in sets/dicts)."""
        pos1 = Position(x=5, y=10)
        pos2 = Position(x=5, y=10)
        pos_set = {pos1, pos2}
        assert len(pos_set) == 1  # Only one unique position


class TestPositionOperations:
    """Test Position arithmetic operations."""

    def test_add_positions(self):
        """Test adding two positions."""
        pos1 = Position(x=5, y=10)
        pos2 = Position(x=3, y=2)
        result = pos1 + pos2
        assert result == Position(x=8, y=12)

    def test_position_zero(self):
        """Test the zero position constant."""
        assert Position.ZERO == Position(x=0, y=0)

    def test_adjacent_positions(self):
        """Test checking if two positions are adjacent."""
        pos = Position(x=5, y=5)

        # Adjacent positions (4 directions)
        assert pos.is_adjacent(Position(x=6, y=5))  # Right
        assert pos.is_adjacent(Position(x=4, y=5))  # Left
        assert pos.is_adjacent(Position(x=5, y=6))  # Down
        assert pos.is_adjacent(Position(x=5, y=4))  # Up

        # Not adjacent
        assert not pos.is_adjacent(Position(x=7, y=5))  # Two steps away
        assert not pos.is_adjacent(Position(x=6, y=6))  # Diagonal

    def test_distance(self):
        """Test Manhattan distance between two positions."""
        pos1 = Position(x=0, y=0)
        pos2 = Position(x=3, y=4)
        assert pos1.distance_to(pos2) == 7  # Manhattan distance

    def test_in_bounds(self):
        """Test checking if position is within bounds."""
        pos = Position(x=5, y=10)

        # Within 20x20 grid
        assert pos.is_in_bounds(width=20, height=20)

        # Out of bounds
        assert not pos.is_in_bounds(width=5, height=20)  # x >= width
        assert not pos.is_in_bounds(width=20, height=10)  # y >= height

        # Edge cases
        edge_pos = Position(x=19, y=19)
        assert edge_pos.is_in_bounds(width=20, height=20)

        corner_pos = Position(x=0, y=0)
        assert corner_pos.is_in_bounds(width=20, height=20)
