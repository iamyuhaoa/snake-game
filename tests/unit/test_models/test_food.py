"""Unit tests for Food model."""

import pytest
from src.models.food import Food
from src.models.position import Position


class TestFoodCreation:
    """Test Food model creation and initialization."""

    def test_create_food_at_position(self):
        """Test creating food at a specific position."""
        position = Position(x=10, y=15)
        food = Food(position=position)
        assert food.position == position

    def test_food_is_immutable(self):
        """Test that Food is immutable (frozen dataclass)."""
        food = Food(position=Position(x=5, y=10))
        with pytest.raises(AttributeError):
            food.position = Position(x=6, y=10)  # type: ignore


class TestFoodGeneration:
    """Test Food generation methods."""

    def test_spawn_at_random_position(self):
        """Test spawning food at a random position within bounds."""
        food = Food.spawn_random(width=20, height=20)

        # Position should be within bounds
        assert 0 <= food.position.x < 20
        assert 0 <= food.position.y < 20

    def test_spawn_avoids_forbidden_positions(self):
        """Test that food doesn't spawn on forbidden positions."""
        forbidden = {Position(x=5, y=5), Position(x=10, y=10)}

        # Spawn food multiple times to verify it never hits forbidden spots
        for _ in range(20):
            food = Food.spawn_random(
                width=20, height=20, forbidden=forbidden
            )
            assert food.position not in forbidden

    def test_spawn_with_large_forbidden_set(self):
        """Test spawning when most positions are forbidden."""
        # Create a scenario where only 1 position is available
        forbidden = {
            Position(x=x, y=y)
            for x in range(20)
            for y in range(20)
            if not (x == 0 and y == 0)
        }

        food = Food.spawn_random(width=20, height=20, forbidden=forbidden)
        assert food.position == Position(x=0, y=0)
