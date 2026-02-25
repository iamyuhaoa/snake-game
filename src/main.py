"""Snake Game - 贪吃蛇

A classic Snake game implementation using Python and Pygame.
"""

import sys
from src.engine.game_loop import GameLoop
from src.config.settings import Settings


def main() -> None:
    """Main entry point for the Snake game."""
    # Load settings
    settings = Settings()

    # Create and run game loop
    game = GameLoop(
        width=settings.GRID_WIDTH,
        height=settings.GRID_HEIGHT,
        fps=settings.FPS
    )

    try:
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
