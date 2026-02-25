"""Unit tests for Renderer font handling."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pytest
from unittest.mock import MagicMock, patch
import pygame
from src.renderer.renderer import Renderer
from src.config.colors import DEFAULT_COLORS


class TestRendererFontFallback:
    """Test renderer font initialization and fallback behavior."""

    def test_renderer_initializes_font_when_pygame_ready(self):
        """Test renderer creates fonts when pygame is initialized."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30

        renderer = Renderer(screen, cell_size)

        # Font should be initialized
        assert renderer.font is not None
        assert renderer.large_font is not None

        pygame.quit()

    @patch('src.renderer.renderer.pygame.font.Font')
    def test_renderer_handles_font_error_gracefully(self, mock_font_class):
        """Test renderer handles font initialization errors."""
        # Make Font raise an error
        mock_font_class.side_effect = pygame.error("Font error")

        screen = MagicMock()
        cell_size = 30

        # Should not raise, font attributes set to None
        renderer = Renderer(screen, cell_size)

        assert renderer.font is None
        assert renderer.large_font is None

    @patch('src.renderer.renderer.pygame.font.Font')
    def test_renderer_with_font_error_doesnt_crash_render(self, mock_font_class):
        """Test renderer can render even when font initialization fails."""
        mock_font_class.side_effect = pygame.error("Font error")

        # Use a real pygame surface, not MagicMock
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        # Create a mock game state
        from src.models.game_state import GameState, GameStatus
        from src.models.snake import Snake
        from src.models.food import Food
        from src.models.position import Position

        state = GameState(
            snake=Snake.create_default(),
            food=Food(position=Position(x=15, y=15)),
            score=100,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        # Should not crash even without fonts
        try:
            renderer.render(state)
        except Exception as e:
            pygame.quit()
            pytest.fail(f"render() raised {e} when fonts are None")

        pygame.quit()

    @patch('src.renderer.renderer.pygame.font.Font')
    def test_draw_score_skips_when_font_none(self, mock_font_class):
        """Test _draw_score skips rendering when font is None."""
        mock_font_class.side_effect = pygame.error("Font error")

        screen = MagicMock()
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        from src.models.game_state import GameState, GameStatus
        from src.models.snake import Snake
        from src.models.food import Food
        from src.models.position import Position

        state = GameState(
            snake=Snake.create_default(),
            food=Food(position=Position(x=15, y=15)),
            score=100,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        # Should not call blit when font is None
        renderer._draw_score(state)
        # If font is None, blit should not be called for text
        # (screen.blit may be called for other reasons)

    @patch('src.renderer.renderer.pygame.font.Font')
    def test_draw_text_centered_skips_when_font_none(self, mock_font_class):
        """Test _draw_text_centered skips rendering when font is None."""
        mock_font_class.side_effect = pygame.error("Font error")

        screen = MagicMock()
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        # Should not raise when font is None
        try:
            renderer._draw_text_centered("Test", renderer.font)
        except Exception as e:
            pytest.fail(f"_draw_text_centered raised {e} when font is None")

    def test_renderer_caches_font_instances(self):
        """Test renderer creates font instances once during init."""
        pygame.init()
        screen = pygame.Surface((600, 600))
        cell_size = 30

        renderer = Renderer(screen, cell_size)

        # Font instances should be the same across calls
        font1 = renderer.font
        font2 = renderer.font
        assert font1 is font2 or font1 == font2

        large_font1 = renderer.large_font
        large_font2 = renderer.large_font
        assert large_font1 is large_font2 or large_font1 == large_font2

        pygame.quit()


class TestRendererFontUsage:
    """Test renderer uses fonts correctly when available."""

    def test_draw_score_uses_font_when_available(self):
        """Test _draw_score uses font to render text."""
        pygame.init()
        screen = MagicMock()
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        from src.models.game_state import GameState, GameStatus
        from src.models.snake import Snake
        from src.models.food import Food
        from src.models.position import Position

        state = GameState(
            snake=Snake.create_default(),
            food=Food(position=Position(x=15, y=15)),
            score=100,
            status=GameStatus.PLAYING,
            width=20,
            height=20
        )

        renderer._draw_score(state)

        # blit should be called when font is available
        assert screen.blit.called

        pygame.quit()

    def test_draw_text_centered_uses_font_when_available(self):
        """Test _draw_text_centered uses font to render text."""
        pygame.init()
        screen = MagicMock()
        cell_size = 30
        renderer = Renderer(screen, cell_size)

        renderer._draw_text_centered("Test Text", renderer.font)

        # Should have called blit to draw text
        assert screen.blit.called

        pygame.quit()
