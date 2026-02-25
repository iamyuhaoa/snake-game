"""Unit tests for collision detection."""

import pytest
from src.engine.collision import CollisionChecker
from src.models.position import Position
from src.models.snake import Snake
from src.models.direction import Direction
from src.models.food import Food


class TestWallCollision:
    """Test wall collision detection."""

    def test_snake_inside_bounds_no_collision(self):
        """Test snake inside grid bounds has no wall collision."""
        body = (Position(x=5, y=10), Position(x=4, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)
        checker = CollisionChecker(width=20, height=20)

        assert not checker.check_wall_collision(snake)

    def test_snake_head_at_right_edge(self):
        """Test snake head at right edge collides with wall."""
        body = (Position(x=19, y=10), Position(x=18, y=10))  # At edge
        snake = Snake(body=body, direction=Direction.RIGHT)
        checker = CollisionChecker(width=20, height=20)

        # Snake already at edge
        assert not checker.check_wall_collision(snake)

        # Snake would move into wall
        next_snake = snake.move(grow=False)
        assert checker.check_wall_collision(next_snake)

    def test_snake_head_at_left_edge(self):
        """Test snake head at left edge collides with wall."""
        body = (Position(x=0, y=10), Position(x=1, y=10))
        snake = Snake(body=body, direction=Direction.LEFT)
        checker = CollisionChecker(width=20, height=20)

        next_snake = snake.move(grow=False)
        assert checker.check_wall_collision(next_snake)

    def test_snake_head_at_top_edge(self):
        """Test snake head at top edge collides with wall."""
        body = (Position(x=10, y=0), Position(x=10, y=1))
        snake = Snake(body=body, direction=Direction.UP)
        checker = CollisionChecker(width=20, height=20)

        next_snake = snake.move(grow=False)
        assert checker.check_wall_collision(next_snake)

    def test_snake_head_at_bottom_edge(self):
        """Test snake head at bottom edge collides with wall."""
        body = (Position(x=10, y=19), Position(x=10, y=18))
        snake = Snake(body=body, direction=Direction.DOWN)
        checker = CollisionChecker(width=20, height=20)

        next_snake = snake.move(grow=False)
        assert checker.check_wall_collision(next_snake)


class TestSelfCollision:
    """Test self-collision detection."""

    def test_snake_no_self_collision(self):
        """Test normal snake has no self collision."""
        snake = Snake.create_default()
        checker = CollisionChecker(width=20, height=20)

        assert not checker.check_self_collision(snake)

    def test_snake_self_collision_detected(self):
        """Test self-collision is detected."""
        # Create snake with duplicate head position
        body = (Position(x=5, y=10), Position(x=5, y=10), Position(x=4, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)
        checker = CollisionChecker(width=20, height=20)

        assert checker.check_self_collision(snake)


class TestFoodCollision:
    """Test food collision detection."""

    def test_snake_eats_food_when_head_on_food(self):
        """Test snake eats food when head position matches food."""
        food_pos = Position(x=5, y=10)
        snake = Snake(body=(food_pos, Position(x=4, y=10)), direction=Direction.RIGHT)
        food = Food(position=food_pos)
        checker = CollisionChecker(width=20, height=20)

        assert checker.check_food_collision(snake, food)

    def test_snake_no_food_collision_when_not_on_food(self):
        """Test no collision when snake head not on food."""
        snake = Snake(
            body=(Position(x=5, y=10), Position(x=4, y=10)),
            direction=Direction.RIGHT
        )
        food = Food(position=Position(x=15, y=15))
        checker = CollisionChecker(width=20, height=20)

        assert not checker.check_food_collision(snake, food)


class TestAnyCollision:
    """Test combined collision checking."""

    def test_no_collision_safe_state(self):
        """Test no collision in safe game state."""
        snake = Snake.create_default()
        food = Food(position=Position(x=15, y=15))
        checker = CollisionChecker(width=20, height=20)

        assert not checker.has_collision(snake, food)

    def test_has_wall_collision(self):
        """Test collision detected when snake hits wall."""
        body = (Position(x=19, y=10), Position(x=18, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)
        next_snake = snake.move(grow=False)
        food = Food(position=Position(x=15, y=15))
        checker = CollisionChecker(width=20, height=20)

        assert checker.has_collision(next_snake, food)

    def test_has_self_collision(self):
        """Test collision detected when snake hits itself."""
        body = (Position(x=5, y=10), Position(x=5, y=10), Position(x=4, y=10))
        snake = Snake(body=body, direction=Direction.RIGHT)
        food = Food(position=Position(x=15, y=15))
        checker = CollisionChecker(width=20, height=20)

        assert checker.has_collision(snake, food)
