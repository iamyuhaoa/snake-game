"""Unit tests for main entry point."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys


class TestMainFunction:
    """Test main() entry point behavior."""

    @patch('src.main.GameLoop')
    def test_main_creates_game_with_settings(self, mock_game_loop_class):
        """Test main creates GameLoop with correct settings."""
        # Import after patching
        from src import main

        # Create a mock game instance
        mock_game = MagicMock()
        mock_game_loop_class.return_value = mock_game

        # Call main
        main.main()

        # Verify GameLoop was created with settings
        mock_game_loop_class.assert_called_once()
        call_args = mock_game_loop_class.call_args

        # Check that settings were passed
        assert call_args.kwargs['width'] == 20
        assert call_args.kwargs['height'] == 20
        assert call_args.kwargs['fps'] == 5

    @patch('src.main.GameLoop')
    def test_main_calls_game_run(self, mock_game_loop_class):
        """Test main calls run() on the game."""
        from src import main

        mock_game = MagicMock()
        mock_game_loop_class.return_value = mock_game

        main.main()

        # Verify run was called
        mock_game.run.assert_called_once()

    @patch('src.main.GameLoop')
    @patch('src.main.sys.exit')
    def test_main_handles_keyboard_interrupt(self, mock_exit, mock_game_loop_class):
        """Test main handles KeyboardInterrupt gracefully."""
        from src import main

        mock_game = MagicMock()
        mock_game.run.side_effect = KeyboardInterrupt()
        mock_game_loop_class.return_value = mock_game

        main.main()

        # Verify clean exit
        mock_exit.assert_called_once_with(0)

    @patch('src.main.GameLoop')
    @patch('src.main.sys.exit')
    @patch('src.main.print')
    def test_main_handles_generic_exceptions(self, mock_print, mock_exit, mock_game_loop_class):
        """Test main handles exceptions with error message."""
        from src import main

        mock_game = MagicMock()
        test_error = RuntimeError("Test error")
        mock_game.run.side_effect = test_error
        mock_game_loop_class.return_value = mock_game

        main.main()

        # Verify error was printed
        mock_print.assert_called()
        error_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error:" in call or "Test error" in call for call in error_calls)

        # Verify error exit code
        mock_exit.assert_called_once_with(1)


class TestMainImports:
    """Test that main module imports correctly."""

    def test_main_module_exists(self):
        """Test that main module can be imported."""
        from src import main

        assert main is not None
        assert hasattr(main, 'main')

    def test_main_function_signature(self):
        """Test main function has correct signature."""
        from src import main
        import inspect

        sig = inspect.signature(main.main)
        assert len(sig.parameters) == 0
        assert sig.return_annotation == None
