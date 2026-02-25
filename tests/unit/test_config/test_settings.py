"""Unit tests for Settings configuration."""

import pytest
from src.config.settings import Settings


class TestSettingsDefaults:
    """Test default settings values."""

    def test_default_grid_settings(self):
        """Test default grid dimensions."""
        settings = Settings()

        assert settings.GRID_WIDTH == 20
        assert settings.GRID_HEIGHT == 20

    def test_default_fps(self):
        """Test default FPS setting."""
        settings = Settings()

        assert settings.FPS == 5

    def test_default_window_size(self):
        """Test default window size."""
        settings = Settings()

        assert settings.WINDOW_SIZE == 600

    def test_default_points_per_food(self):
        """Test default points per food."""
        settings = Settings()

        assert settings.POINTS_PER_FOOD == 10


class TestSettingsCustomization:
    """Test settings customization."""

    def test_custom_grid_size(self):
        """Test creating settings with custom grid size."""
        settings = Settings(
            GRID_WIDTH=30,
            GRID_HEIGHT=15
        )

        assert settings.GRID_WIDTH == 30
        assert settings.GRID_HEIGHT == 15

    def test_custom_fps(self):
        """Test creating settings with custom FPS."""
        settings = Settings(FPS=10)

        assert settings.FPS == 10

    def test_custom_window_size(self):
        """Test creating settings with custom window size."""
        settings = Settings(WINDOW_SIZE=800)

        assert settings.WINDOW_SIZE == 800

    def test_multiple_custom_settings(self):
        """Test settings with multiple custom values."""
        settings = Settings(
            GRID_WIDTH=25,
            GRID_HEIGHT=25,
            FPS=15,
            POINTS_PER_FOOD=20
        )

        assert settings.GRID_WIDTH == 25
        assert settings.GRID_HEIGHT == 25
        assert settings.FPS == 15
        assert settings.POINTS_PER_FOOD == 20


class TestSettingsImmutability:
    """Test settings dataclass properties."""

    def test_settings_is_dataclass(self):
        """Test that Settings is a dataclass."""
        from dataclasses import is_dataclass

        assert is_dataclass(Settings)

    def test_settings_attributes(self):
        """Test settings has expected attributes."""
        settings = Settings()

        assert hasattr(settings, 'GRID_WIDTH')
        assert hasattr(settings, 'GRID_HEIGHT')
        assert hasattr(settings, 'FPS')
        assert hasattr(settings, 'WINDOW_SIZE')
        assert hasattr(settings, 'POINTS_PER_FOOD')
