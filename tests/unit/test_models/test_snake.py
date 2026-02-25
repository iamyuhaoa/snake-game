"""Unit tests for Snake model."""

import pytest
from src.models.snake import Snake
from src.models.position import Position
from src.models.direction import Direction


class TestSnakeCreation:
    """Test Snake model creation and initialization."""

    def test_create_snake_with_body_and_direction(self):
        """Test creating a snake with body segments and direction."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        assert snake.body == body
        assert snake.direction == Direction.RIGHT

    def test_snake_head_is_first_segment(self):
        """Test that snake head is the first body segment."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        assert snake.head == Position(x=5, y=10)

    def test_snake_length(self):
        """Test getting snake length."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        assert len(snake) == 3

    def test_create_default_snake(self):
        """Test creating a default snake with 3 segments."""
        snake = Snake.create_default()

        assert len(snake) == 3
        assert snake.direction == Direction.RIGHT


class TestSnakeMovement:
    """Test Snake movement logic."""

    def test_move_forward_without_eating(self):
        """Test moving forward without eating (tail removed)."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        new_snake = snake.move(grow=False)

        # Head moves to new position
        assert new_snake.head == Position(x=6, y=10)
        # Tail is removed
        assert len(new_snake) == 3
        # Old tail position is removed
        assert Position(x=3, y=10) not in new_snake.body

    def test_grow_increases_length(self):
        """Test growing the snake increases length by 1."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        grown_snake = snake.grow()

        assert len(grown_snake) == len(snake) + 1
        # New segment is a duplicate of the old tail
        assert grown_snake.body[-1] == Position(x=3, y=10)
        # Tail segment appears twice at the end
        assert grown_snake.body[-2] == Position(x=3, y=10)

    def test_move_forward_with_eating(self):
        """Test moving forward while eating (tail preserved)."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        new_snake = snake.move(grow=True)

        # Head moves to new position
        assert new_snake.head == Position(x=6, y=10)
        # Tail is preserved (snake grows)
        assert len(new_snake) == 4
        # Old tail position is preserved
        assert Position(x=3, y=10) in new_snake.body

    def test_move_in_all_directions(self):
        """Test moving in all four directions."""
        center = Position(x=10, y=10)

        # Move UP
        snake = Snake(body=(center,), direction=Direction.UP)
        assert snake.move(grow=False).head == Position(x=10, y=9)

        # Move DOWN
        snake = Snake(body=(center,), direction=Direction.DOWN)
        assert snake.move(grow=False).head == Position(x=10, y=11)

        # Move LEFT
        snake = Snake(body=(center,), direction=Direction.LEFT)
        assert snake.move(grow=False).head == Position(x=9, y=10)

        # Move RIGHT
        snake = Snake(body=(center,), direction=Direction.RIGHT)
        assert snake.move(grow=False).head == Position(x=11, y=10)


class TestSnakeDirectionChange:
    """Test Snake direction changing logic."""

    def test_change_to_valid_direction(self):
        """Test changing to a valid direction."""
        snake = Snake(
            body=(Position(x=5, y=10),), direction=Direction.RIGHT
        )
        new_snake = snake.change_direction(Direction.UP)

        assert new_snake.direction == Direction.UP

    def test_cannot_reverse_directly(self):
        """Test that snake cannot directly reverse direction."""
        snake = Snake(
            body=(Position(x=5, y=10),), direction=Direction.RIGHT
        )

        # Try to reverse (should ignore)
        new_snake = snake.change_direction(Direction.LEFT)

        assert new_snake.direction == Direction.RIGHT  # Direction unchanged

    def test_perpendicular_directions_allowed(self):
        """Test that perpendicular direction changes are allowed."""
        snake = Snake(
            body=(Position(x=5, y=10),), direction=Direction.RIGHT
        )

        # UP and DOWN should both be allowed
        assert snake.change_direction(Direction.UP).direction == Direction.UP
        assert snake.change_direction(Direction.DOWN).direction == Direction.DOWN


class TestSnakeCollision:
    """Test Snake collision detection."""

    def test_check_self_collision(self):
        """Test detecting when snake collides with itself."""
        # Create a snake body where the head position also appears later
        # This simulates a snake that has turned into its own path
        body = (
            Position(x=5, y=10),  # head
            Position(x=5, y=10),  # head appears again (collision!)
            Position(x=4, y=10),
        )
        snake = Snake(body=body, direction=Direction.RIGHT)
        assert snake.collides_with_self()

    def test_no_self_collision_normal_state(self):
        """Test that normal snake state has no self collision."""
        body = (Position(x=5, y=10), Position(x=4, y=10), Position(x=3, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        assert not snake.collides_with_self()


class TestSnakeBodyPositionSet:
    """Test Snake body position utilities."""

    def test_body_as_set(self):
        """Test getting body positions as a set."""
        body = (
            Position(x=5, y=10),
            Position(x=4, y=10),
            Position(x=3, y=10),
        )
        snake = Snake(body=body, direction=Direction.RIGHT)

        body_set = snake.body_positions
        assert len(body_set) == 3
        assert Position(x=5, y=10) in body_set
        assert Position(x=4, y=10) in body_set
        assert Position(x=3, y=10) in body_set

    def test_head_in_body_positions(self):
        """Test that head is included in body positions."""
        body = (Position(x=5, y=10), Position(x=4, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)

        assert snake.head in snake.body_positions


class TestSnakeContainsPosition:
    """Test checking if snake contains a position."""

    def test_contains_head(self):
        """Test that snake contains its head position."""
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        assert snake.contains(Position(x=5, y=10))

    def test_contains_body(self):
        """Test that snake contains its body positions."""
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        assert snake.contains(Position(x=4, y=10))

    def test_does_not_contain_other_positions(self):
        """Test that snake doesn't contain unrelated positions."""
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        assert not snake.contains(Position(x=10, y=10))
