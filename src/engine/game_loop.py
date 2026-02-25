"""Game loop for the Snake game."""

import pygame
from src.models.game_state import GameState, GameStatus
from src.engine.collision import CollisionChecker
from src.engine.input_handler import InputHandler, InputAction
from src.models.direction import Direction
from typing import Optional


class GameLoop:
    """Main game loop controller."""

    def __init__(self, width: int = 20, height: int = 20, fps: int = 5) -> None:
        """Initialize game loop.

        Args:
            width: Grid width (number of columns).
            height: Grid height (number of rows).
            fps: Target frames per second (game speed).
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.state = GameState.create_initial(width, height)
        self.collision_checker = CollisionChecker(width, height)
        self.input_handler = InputHandler()
        self.pending_direction: Optional[Direction] = None

    def handle_input(self, action: InputAction) -> None:
        """Handle an input action.

        Args:
            action: The input action to handle.
        """
        if action == InputAction.QUIT:
            self.state = self.state.game_over()
        elif action == InputAction.RESTART:
            self.state = GameState.create_initial(self.width, self.height)
            self.pending_direction = None
        elif action == InputAction.PAUSE:
            if self.state.status == GameStatus.PLAYING:
                self.state = self.state.pause()
            elif self.state.status == GameStatus.PAUSED:
                self.state = self.state.resume()
        elif self.state.is_playing():
            # Movement input - store as pending
            direction = InputAction.to_direction(action)
            if direction:
                self.pending_direction = direction

    def update(self) -> None:
        """Update game state by one tick."""
        # Don't update if paused or game over
        if not self.state.is_playing():
            return

        # Apply pending direction change
        if self.pending_direction:
            self.state = self.state.change_direction(self.pending_direction)
            self.pending_direction = None

        # Move snake
        self.state = self.state.move_snake(grow=False)

        # Check if snake head is on food (after moving)
        eats_food = self.collision_checker.check_food_collision(
            self.state.snake, self.state.food
        )

        if eats_food:
            # Snake ate food - increase score and respawn food
            # Note: move_snake was called with grow=False, so we need to add the tail back
            # and increase the score. Let's create a new state with the grown snake
            from src.models.snake import Snake

            # Reconstruct the snake with growth (add tail segment back)
            old_tail = self.state.snake.body[-1]
            new_body = self.state.snake.body + (old_tail,)
            grown_snake = Snake(body=new_body, direction=self.state.snake.direction)

            self.state = self.state.__class__(
                snake=grown_snake,
                food=self.state.food,
                score=self.state.score + 10,
                status=self.state.status,
                width=self.state.width,
                height=self.state.height
            ).respawn_food()

        # Check for collisions (wall or self)
        if self.collision_checker.has_collision(self.state.snake, self.state.food):
            self.state = self.state.game_over()

    def run(self) -> None:
        """Run the main game loop (blocking).

        This method initializes pygame and runs the game loop
        until the game is over or user quits.
        """
        # Initialize pygame
        pygame.init()
        clock = pygame.time.Clock()

        # Calculate cell size based on screen size
        SCREEN_SIZE = 600
        cell_size = SCREEN_SIZE // max(self.width, self.height)

        # Create window
        screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("贪吃蛇 - Snake Game")

        # Import renderer here to avoid pygame issues in tests
        from src.renderer.renderer import Renderer

        renderer = Renderer(screen, cell_size)

        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    action = self.input_handler.handle_key(event.key)
                    if action == InputAction.QUIT:
                        running = False
                    else:
                        self.handle_input(action)

            # Update game state
            self.update()

            # Render
            renderer.render(self.state)

            # Cap framerate
            clock.tick(self.fps)

            # Check if game over and user wants to quit
            if self.state.is_over():
                # Brief pause before potentially closing
                pygame.time.delay(1000)

        pygame.quit()
