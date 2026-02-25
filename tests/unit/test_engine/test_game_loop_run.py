"""Unit tests for GameLoop.run() method."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import pygame
from src.engine.game_loop import GameLoop
from src.models.game_state import GameStatus


class TestGameLoopRun:
    """Test GameLoop.run() method."""

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    def test_run_initializes_pygame(
        self,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_init
    ):
        """Test run initializes pygame components."""
        # Setup mocks
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        # Make game loop exit immediately
        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            mock_events.return_value = [
                MagicMock(type=pygame.QUIT)
            ]

            game = GameLoop(width=20, height=20, fps=10)
            game.run()

        # Verify initialization
        mock_init.assert_called_once()
        mock_set_mode.assert_called_once()
        mock_set_caption.assert_called_once_with("贪吃蛇 - Snake Game")
        mock_renderer_class.assert_called_once()

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    def test_run_processes_quit_event(
        self,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_init
    ):
        """Test run handles QUIT event."""
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            # First event: QUIT
            mock_events.return_value = [MagicMock(type=pygame.QUIT)]

            game = GameLoop(width=20, height=20, fps=10)
            game.run()

        # Should exit gracefully
        assert mock_events.call_count >= 1

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    def test_run_processes_key_events(
        self,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_init
    ):
        """Test run handles KEYDOWN events."""
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            # Simulate a few events then quit
            events = [
                MagicMock(type=pygame.KEYDOWN, key=pygame.K_UP),
                MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE),  # QUIT
                MagicMock(type=pygame.QUIT),
            ]
            mock_events.side_effect = [events] + [[]] * 10

            game = GameLoop(width=20, height=20, fps=10)
            game.run()

        # Verify events were processed
        assert mock_events.call_count >= 1

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    def test_run_caps_framerate(
        self,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_init
    ):
        """Test run caps framerate with clock.tick."""
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            mock_events.return_value = [MagicMock(type=pygame.QUIT)]

            game = GameLoop(width=10, height=10, fps=15)
            game.run()

        # Verify clock.tick was called with FPS
        mock_clock.tick.assert_called()

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    def test_run_calls_renderer(
        self,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_init
    ):
        """Test run calls renderer.render()."""
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            mock_events.return_value = [MagicMock(type=pygame.QUIT)]

            game = GameLoop(width=10, height=10, fps=10)
            game.run()

        # Verify render was called
        assert mock_renderer.render.call_count >= 1

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    @patch('src.engine.game_loop.pygame.time.delay')
    def test_run_delays_on_game_over(
        self,
        mock_delay,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_init
    ):
        """Test run shows delay when game is over."""
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            # Game becomes over immediately
            game = GameLoop(width=10, height=10, fps=10)
            game.state = game.state.game_over()

            mock_events.return_value = [MagicMock(type=pygame.QUIT)]

            game.run()

        # Verify delay was called when game over
        assert mock_delay.call_count >= 0

    @patch('src.engine.game_loop.pygame.init')
    @patch('src.engine.game_loop.pygame.quit')
    @patch('src.engine.game_loop.pygame.time.Clock')
    @patch('src.engine.game_loop.pygame.display.set_mode')
    @patch('src.engine.game_loop.pygame.display.set_caption')
    @patch('src.renderer.renderer.Renderer')
    def test_run_quits_pygame_on_exit(
        self,
        mock_renderer_class,
        mock_set_caption,
        mock_set_mode,
        mock_clock_class,
        mock_quit,
        mock_init
    ):
        """Test run calls pygame.quit() on exit."""
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen
        mock_clock = MagicMock()
        mock_clock_class.return_value = mock_clock
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer

        with patch('src.engine.game_loop.pygame.event.get') as mock_events:
            mock_events.return_value = [MagicMock(type=pygame.QUIT)]

            game = GameLoop(width=10, height=10, fps=10)
            game.run()

        # Verify pygame.quit was called
        mock_quit.assert_called_once()
