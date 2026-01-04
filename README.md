# Crossword Puzzle Game

A feature-rich, object-oriented crossword puzzle game built with Python and Tkinter. This project demonstrates clean architecture principles with a modular design that separates concerns across models, services, engine, and GUI layers.

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎮 Overview

This crossword puzzle game provides an interactive interface for solving dynamically generated crossword puzzles. The application fetches words from a configurable data pipeline, intelligently places them on a grid using advanced placement algorithms, and provides real-time validation and hints as users solve the puzzle.

### Key Features

- **Dynamic Puzzle Generation**: Automatically generates puzzles from a word database
- **Multiple Placement Strategies**: Supports different algorithms for word placement (intersection-based, backtracking)
- **Real-time Validation**: Instant feedback on solution correctness
- **Interactive Grid**: Click-to-select cells with automatic word highlighting
- **Smart Clue System**: Organized across/down clues with synchronized highlighting
- **Hint System**: Get help when stuck on specific words
- **Progress Tracking**: Visual feedback on completion status
- **Customizable Difficulty**: Configurable grid sizes and word counts

## 📁 Project Structure

```
crossword_game/
│
├── main.py                          # Application entry point
│
├── models/                          # Data models and domain objects
│   ├── __init__.py
│   ├── word.py                      # CrosswordWord and Direction enum
|   ├── cell.py                      # Cell and CellType models
│   ├── grid.py                      # Grid model
│   ├── puzzle.py                    # Puzzle and PuzzleMetadata
│   └── clue.py                      # Clue model
│
├── services/                        # Business logic services
│   ├── __init__.py
│   ├── data_pipeline.py             # Word fetching from data source
│   ├── puzzle_builder.py            # Puzzle construction and layout
│   └── validator.py                 # Solution validation logic
│
├── engine/                          # Core game engine
│   ├── __init__.py
│   ├── crossword_engine.py          # Main orchestrator
│   └── placement_algorithm.py       # Word placement strategies
│
├── gui/                             # User interface components
│   ├── __init__.py
│   ├── main_window.py               # Main application window
│   ├── grid_view.py                 # Grid display and interaction
│   ├── clues_view.py                # Clues panel
│   └── controls.py                  # Control buttons and actions
│
├── config/                          # Configuration
│   ├── __init__.py
│   └── settings.py                  # Application settings
│
├── tests/                           # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_engine.py
│
└── README.md
```

## 🏗️ Architecture

The application follows a **layered architecture** with clear separation of concerns:

### 1. Models Layer
Pure data structures representing the domain:

- **`CrosswordWord`**: Represents a word with position, direction, and clue
  - Calculates character positions and intersections
  - Validates word placement constraints
  
- **`Grid`**: Manages the puzzle grid structure
  - Provides cell-level operations
  - Supports deep copying for state management
  
- **`Cell`**: Individual grid cell with letter, type, and numbering
  - Tracks word start positions
  - Distinguishes between letter cells and black squares
  
- **`Puzzle`**: Complete puzzle container
  - Holds grid, words, and metadata
  - Validates puzzle structure integrity
  
- **`Clue`**: Represents individual clues with validation

### 2. Services Layer
Isolated business logic components:

- **`DataPipelineService`**: Fetches words from external data source
  - Supports filtering by difficulty, category, and theme
  - Implements caching for performance
  - Configurable API endpoint integration
  
- **`PuzzleBuilderService`**: Constructs puzzles from words
  - Places words on grid using configurable strategies
  - Assigns clue numbers automatically
  - Validates puzzle completeness and solvability
  
- **`ValidationService`**: Validates user solutions
  - Compares user input against solution
  - Identifies specific errors by position
  - Calculates completion percentage

### 3. Engine Layer
Core game logic orchestration:

- **`CrosswordEngine`**: Central coordinator
  - Manages puzzle state and user progress
  - Coordinates service interactions
  - Provides high-level game operations
  - Tracks current puzzle and user grid
  
- **`PlacementStrategy`**: Abstract interface for word placement
  - **`IntersectionStrategy`**: Places words by finding character matches
  - **`BacktrackingStrategy`**: Uses backtracking for optimal placement

### 4. GUI Layer
User interface components:

- **`MainWindow`**: Application container
  - Layout management
  - Event routing to engine
  
- **`GridView`**: Interactive puzzle grid
  - Cell rendering and input handling
  - Word and cell highlighting
  - Visual feedback for errors
  
- **`CluesView`**: Clue display panel
  - Organized across/down sections
  - Synchronized highlighting with grid
  
- **`ControlPanel`**: Action buttons
  - New puzzle, check solution, hints, reset

## 🔄 Data Flow

```
User Action → GUI Component → Engine → Service(s) → Models → Engine → GUI Update
```

**Example: Generating a New Puzzle**
1. User clicks "New Puzzle" button
2. `MainWindow` calls `engine.generate_new_puzzle()`
3. Engine calls `DataPipelineService.fetch_words()`
4. Engine calls `PuzzleBuilderService.build_puzzle()`
5. Builder creates `Grid`, places `CrosswordWord` objects
6. Engine stores `Puzzle` and creates empty user grid
7. GUI components render the puzzle

## 🎯 Key Design Principles

### Separation of Concerns
- Models contain no business logic
- Services have no UI dependencies
- Engine orchestrates without UI knowledge
- GUI only interacts with engine

### Dependency Injection
Components receive dependencies rather than creating them:
```python
engine = CrosswordEngine(
    data_service=DataPipelineService(),
    builder_service=PuzzleBuilderService(),
    validator_service=ValidationService()
)
```

### Strategy Pattern
Word placement algorithms are interchangeable:
```python
builder = PuzzleBuilderService(strategy=IntersectionStrategy())
# or
builder = PuzzleBuilderService(strategy=BacktrackingStrategy())
```

### Immutability & Validation
Models validate data on construction and provide immutable properties:
```python
word = CrosswordWord("python", "A language", 5, 3, Direction.ACROSS)
# Automatically validates and normalizes to "PYTHON"
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Tkinter (usually included with Python)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crossword-game.git
cd crossword-game
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

3. Configure your data pipeline in `services/data_pipeline.py`:
```python
class DataPipelineService:
    def __init__(self):
        self.api_endpoint = "your_api_endpoint_here"
        # Configure your data source
```

### Running the Application

```bash
python main.py
```

## 🎮 How to Play

1. **Start a New Puzzle**: Click "New Puzzle" to generate a random crossword
2. **Select a Cell**: Click any white cell to start entering letters
3. **Enter Letters**: Type to fill in your answer
4. **Navigate**: 
   - Arrow keys to move between cells
   - Tab to switch between across/down words
5. **Get Help**: Click "Hint" to reveal a letter
6. **Check Your Work**: Click "Check Solution" to validate your answers
7. **Reset**: Click "Reset" to clear all entries and start over

## 🔧 Configuration

Edit `config/settings.py` to customize:

```python
class Settings:
    GRID_SIZE = 15              # Grid dimensions
    CELL_SIZE = 30              # Cell pixel size
    MAX_WORDS = 20              # Maximum words per puzzle
    API_ENDPOINT = "..."        # Data pipeline URL
    DEFAULT_DIFFICULTY = 3      # 1-5 difficulty scale
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific test modules:
```bash
python -m pytest tests/test_models.py
python -m pytest tests/test_services.py
python -m pytest tests/test_engine.py
```

## 📊 UML Diagrams

### Class Diagram
The project includes comprehensive UML documentation:
- Full class hierarchy with relationships
- Service interactions and dependencies
- Model compositions and associations

### Sequence Diagrams
Key interaction flows:
- Puzzle generation workflow
- User input handling
- Solution validation process
- Hint system operation

See `/docs/diagrams/` for detailed visual documentation.

## 🛠️ Extending the Game

### Adding a New Word Placement Strategy

1. Create a new strategy class in `engine/placement_algorithm.py`:
```python
class MyCustomStrategy(PlacementStrategy):
    def place_words(self, grid: Grid, words: List[Dict]) -> bool:
        # Your custom placement logic
        pass
```

2. Use it in puzzle generation:
```python
builder = PuzzleBuilderService(strategy=MyCustomStrategy())
```

### Adding a New Data Source

1. Implement the data pipeline interface in `services/data_pipeline.py`:
```python
class MyDataPipelineService:
    def fetch_words(self, count: int, difficulty: str) -> List[Dict]:
        # Fetch from your custom source
        pass
```

2. Inject it into the engine:
```python
engine = CrosswordEngine(data_service=MyDataPipelineService(), ...)
```

### Adding New GUI Features

1. Create a new component in `gui/`:
```python
class TimerView:
    def __init__(self, parent):
        # Timer display logic
        pass
```

2. Integrate it in `MainWindow`:
```python
self.timer = TimerView(self.root)
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new functionality
4. Ensure all tests pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for classes and public methods
- Keep functions focused and under 50 lines when possible

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Crossword puzzle generation inspired by traditional crossword construction techniques
- Architecture based on clean architecture and domain-driven design principles
- GUI built with Python's Tkinter framework

## 📧 Contact

Tamman Montanaro - [@LinkedIn](https://www.linkedin.com/in/tamman-montanaro-38266b144/)

Project Link: [https://github.com/tammanmonty/crossword-game-engine-repo](https://github.com/tammanmonty/crossword-game-engine-repo)

---

**Happy Puzzling! 🧩**
