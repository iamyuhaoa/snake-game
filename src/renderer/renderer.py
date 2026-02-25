"""Renderer for the Snake game."""

import pygame
from src.models.game_state import GameState, GameStatus
from src.config.colors import Colors, DEFAULT_COLORS
from typing import Tuple


class Renderer:
    """Renders the game state to screen."""

    def __init__(self, screen: pygame.Surface, cell_size: int, colors: Colors = DEFAULT_COLORS) -> None:
        """Initialize renderer.

        Args:
            screen: Pygame surface to render to.
            cell_size: Size of each grid cell in pixels.
            colors: Color scheme to use.
        """
        self.screen = screen
        self.cell_size = cell_size
        self.colors = colors

        # Initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()

        # Initialize font
        try:
            self.font = pygame.font.Font(None, 36)
            self.large_font = pygame.font.Font(None, 72)
        except pygame.error:
            # Fallback for headless environments
            self.font = None
            self.large_font = None

    def render(self, state: GameState) -> None:
        """Render the current game state.

        Args:
            state: The game state to render.
        """
        # Clear screen
        self.screen.fill(self.colors.BACKGROUND)

        # Draw game elements
        self._draw_snake(state.snake)
        self._draw_food(state.food)
        self._draw_score(state)

        # Draw overlay if paused or game over
        if state.status == GameStatus.PAUSED:
            self._draw_text_centered("PAUSED", self.large_font)
        elif state.status == GameStatus.GAME_OVER:
            self._draw_text_centered("GAME OVER", self.large_font)
            self._draw_text_centered("Press R to Restart", self.font, offset=50)

        # Update display only if screen is the actual display
        try:
            pygame.display.flip()
        except pygame.error:
            # Screen is not the actual display (e.g., in tests)
            pass

    def _draw_snake(self, snake) -> None:
        """Draw the snake.

        Args:
            snake: The snake to draw.
        """
        for i, segment in enumerate(snake.body):
            x, y, width, height = self._cell_to_rect(segment)

            # Head uses different color
            color = self.colors.SNAKE_HEAD if i == 0 else self.colors.SNAKE_BODY

            # Draw segment with border
            pygame.draw.rect(self.screen, color, (x, y, width, height))
            pygame.draw.rect(
                self.screen,
                self.colors.SNAKE_BORDER,
                (x, y, width, height),
                2  # Border width
            )

    def _draw_food(self, food) -> None:
        """Draw the food.

        Args:
            food: The food to draw.
        """
        x, y, width, height = self._cell_to_rect(food.position)

        # Draw food as a circle
        center_x = x + width // 2
        center_y = y + height // 2
        radius = min(width, height) // 2 - 2

        pygame.draw.circle(
            self.screen,
            self.colors.FOOD,
            (center_x, center_y),
            radius
        )

    def _draw_score(self, state: GameState) -> None:
        """Draw the score.

        Args:
            state: Game state containing score.
        """
        if self.font is None:
            return

        score_text = f"Score: {state.score}"
        text_surface = self.font.render(score_text, True, self.colors.TEXT_PRIMARY)

        # Draw in top-left corner
        self.screen.blit(text_surface, (10, 10))

    def _draw_text_centered(self, text: str, font: pygame.font.Font, offset: int = 0) -> None:
        """Draw centered text overlay.

        Args:
            text: Text to draw.
            font: Font to use.
            offset: Vertical offset from center.
        """
        if font is None:
            return

        text_surface = font.render(text, True, self.colors.TEXT_PRIMARY)
        rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + offset))

        # Draw with semi-transparent background
        bg_rect = rect.inflate(20, 20)
        s = pygame.Surface((bg_rect.width, bg_rect.height))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, bg_rect.topleft)

        self.screen.blit(text_surface, rect)

    def _cell_to_rect(self, position) -> Tuple[int, int, int, int]:
        """Convert grid position to pixel rectangle.

        Args:
            position: Grid position.

        Returns:
            Tuple of (x, y, width, height) in pixels.
        """
        x = position.x * self.cell_size
        y = position.y * self.cell_size
        return (x, y, self.cell_size, self.cell_size)
