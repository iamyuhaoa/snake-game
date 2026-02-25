# 贪吃蛇 (Snake Game)

A classic Snake game implementation in Python using Pygame, following TDD principles.

## Features

- **Classic Snake Gameplay**: Control a snake to eat food and grow longer
- **Score Tracking**: Earn 10 points for each food eaten
- **Collision Detection**: Game ends when hitting walls or the snake itself
- **Pause/Resume**: Press SPACE to pause or resume the game
- **Restart**: Press R to restart the game after game over
- **Smooth Controls**: Arrow keys or WASD for movement, Q/ESC to quit

## Requirements

- Python 3.9+
- Pygame 2.6+

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -r requirements-dev.txt
```

## How to Play

### Controls

| Key | Action |
|-----|--------|
| ↑ / W | Move Up |
| ↓ / S | Move Down |
| ← / A | Move Left |
| → / D | Move Right |
| SPACE | Pause/Resume |
| R | Restart |
| Q / ESC | Quit |

### Rules

- Eat food (red circle) to grow and earn 10 points
- Avoid hitting the walls
- Avoid hitting your own body
- The snake cannot directly reverse direction

## Running the Game

```bash
python src/main.py
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models/test_snake.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Project Structure

```
snake-game/
├── src/
│   ├── main.py                 # Game entry point
│   ├── models/                 # Data models
│   │   ├── position.py         # Grid position
│   │   ├── direction.py        # Movement direction
│   │   ├── snake.py            # Snake entity
│   │   ├── food.py             # Food entity
│   │   └── game_state.py       # Game state
│   ├── engine/                 # Game logic
│   │   ├── collision.py        # Collision detection
│   │   ├── game_loop.py        # Main game loop
│   │   └── input_handler.py    # Input handling
│   ├── renderer/               # Rendering
│   │   └── renderer.py         # Game renderer
│   └── config/                 # Configuration
│       ├── settings.py         # Game settings
│       └── colors.py           # Color scheme
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Development dependencies
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Testing

This project follows **Test-Driven Development (TDD)** principles. All code is written with comprehensive tests:

- **90+ unit tests** covering all models and game logic
- **80%+ code coverage** target
- Tests for edge cases, collision detection, and user input

## License

MIT License

## Credits

Developed with Claude Code using TDD methodology.
