"""Unit tests for Renderer."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from src.renderer.renderer import Renderer
from src.config.colors import DEFAULT_COLORS
from src.models.game_state import GameState, GameStatus
from src.models.position import Position
from src.models.direction import Direction


class TestRendererInitialization:
    """Test Renderer initialization."""

    def test_create_renderer(self):
        """Test creating a renderer instance."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30

        renderer = Renderer(screen, cell_size)

        assert renderer.screen == screen
        assert renderer.cell_size == cell_size
        assert renderer.colors == DEFAULT_COLORS

        pygame.quit()


class TestRendering:
    """Test rendering methods."""

    def test_render_without_crashing(self):
        """Test render executes without errors."""
        # Create real pygame surface for testing
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        state = GameState.create_initial(width=20, height=20)

        # Should not raise
        renderer.render(state)

        pygame.quit()

    def test_render_game_over(self):
        """Test rendering game over state."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        state = GameState.create_initial(width=20, height=20).game_over()

        # Should not raise
        renderer.render(state)

        pygame.quit()

    def test_render_paused(self):
        """Test rendering paused state."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        state = GameState.create_initial(width=20, height=20).pause()

        # Should not raise
        renderer.render(state)

        pygame.quit()


class TestDrawingMethods:
    """Test individual drawing methods."""

    def test_draw_snake(self):
        """Test drawing snake."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        from src.models.snake import Snake
        snake = Snake.create_default()

        # Should not raise
        renderer._draw_snake(snake)

        pygame.quit()

    def test_draw_food(self):
        """Test drawing food."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        from src.models.food import Food
        food = Food(position=Position(x=10, y=10))

        # Should not raise
        renderer._draw_food(food)

        pygame.quit()

    def test_draw_score(self):
        """Test drawing score."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        state = GameState.create_initial(width=20, height=20)
        state = state.with_score(100)

        # Should not raise
        renderer._draw_score(state)

        pygame.quit()

    def test_cell_to_pixel_conversion(self):
        """Test converting grid position to pixel coordinates."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        pos = Position(x=5, y=10)
        x, y, width, height = renderer._cell_to_rect(pos)

        assert x == 5 * cell_size
        assert y == 10 * cell_size
        assert width == cell_size
        assert height == cell_size

        pygame.quit()
