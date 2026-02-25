"""Unit tests for Food edge cases."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pytest
from src.models.food import Food
from src.models.position import Position


class TestFoodEdgeCases:
    """Test Food spawning edge cases."""

    def test_spawn_in_tiny_grid_1x1(self):
        """Test spawning food in a 1x1 grid."""
        food = Food.spawn_random(width=1, height=1)

        assert food.position == Position(x=0, y=0)

    def test_spawn_in_small_grid_2x2(self):
        """Test spawning food in a 2x2 grid."""
        food = Food.spawn_random(width=2, height=2)

        # Position should be one of 4 valid positions
        assert 0 <= food.position.x < 2
        assert 0 <= food.position.y < 2

    def test_spawn_in_rectangular_grid(self):
        """Test spawning food in rectangular (non-square) grid."""
        food = Food.spawn_random(width=30, height=10)

        assert 0 <= food.position.x < 30
        assert 0 <= food.position.y < 10

    def test_spawn_all_positions_forbidden_raises_error(self):
        """Test spawn_random raises ValueError when all positions are forbidden."""
        from src.models.snake import Snake
        from src.models.position import Position

        # Create a snake that fills the entire grid
        all_positions = [
            Position(x=x, y=y)
            for x in range(5)
            for y in range(5)
        ]

        # All positions are forbidden
        with pytest.raises(ValueError, match="No valid position"):
            Food.spawn_random(width=5, height=5, forbidden=all_positions)

    def test_spawn_single_available_position(self):
        """Test spawning when only one position is available."""
        # Forbidden all positions except one
        forbidden = {
            Position(x=x, y=y)
            for x in range(5)
            for y in range(5)
            if not (x == 2 and y == 2)
        }

        food = Food.spawn_random(width=5, height=5, forbidden=forbidden)

        # Must spawn at the only available position
        assert food.position == Position(x=2, y=2)

    def test_spawn_empty_forbidden_list(self):
        """Test spawn_random with empty forbidden list."""
        food = Food.spawn_random(width=10, height=10, forbidden=[])

        # Should spawn somewhere in the grid
        assert 0 <= food.position.x < 10
        assert 0 <= food.position.y < 10

    def test_spawn_none_forbidden(self):
        """Test spawn_random with forbidden=None."""
        food = Food.spawn_random(width=10, height=10, forbidden=None)

        # Should spawn somewhere in the grid
        assert 0 <= food.position.x < 10
        assert 0 <= food.position.y < 10

    def test_spawn_avoids_single_forbidden_position(self):
        """Test spawn_random avoids a single forbidden position."""
        forbidden = {Position(x=5, y=5)}

        # Spawn many times, should never hit forbidden position
        for _ in range(20):
            food = Food.spawn_random(width=10, height=10, forbidden=forbidden)
            assert food.position != Position(x=5, y=5)


class TestFoodEqualityAndHashing:
    """Test Food equality and hashing for use in sets/dicts."""

    def test_two_foods_same_position_are_equal(self):
        """Test two foods at same position are equal."""
        pos = Position(x=10, y=10)
        food1 = Food(position=pos)
        food2 = Food(position=pos)

        assert food1 == food2

    def test_two_foods_different_position_not_equal(self):
        """Test foods at different positions are not equal."""
        food1 = Food(position=Position(x=10, y=10))
        food2 = Food(position=Position(x=11, y=10))

        assert food1 != food2

    def test_food_is_hashable(self):
        """Test Food can be used in sets and dicts."""
        food1 = Food(position=Position(x=10, y=10))
        food2 = Food(position=Position(x=11, y=10))

        food_set = {food1, food2}

        assert len(food_set) == 2

    def test_duplicate_foods_in_set(self):
        """Test duplicate foods (same position) collapse in set."""
        pos = Position(x=10, y=10)
        food1 = Food(position=pos)
        food2 = Food(position=pos)

        food_set = {food1, food2}

        assert len(food_set) == 1


class TestFoodStringRepresentation:
    """Test Food string representation."""

    def test_food_repr(self):
        """Test Food has a useful string representation."""
        food = Food(position=Position(x=5, y=10))

        repr_str = repr(food)

        assert "Food" in repr_str
        assert "5" in repr_str
        assert "10" in repr_str

    def test_food_str(self):
        """Test Food str representation."""
        food = Food(position=Position(x=5, y=10))

        str_str = str(food)

        # Should contain position info
        assert "5" in str_str or "Food" in str_str
