"""
Puzzle model representing a complete crossword puzzle
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from app.models import Grid, Direction, CrosswordWord, Clue

@dataclass
class PuzzleMetaData:
    """
    Metadata about the puzzle.

    title: The title of the puzzle
    author: Puzzle Creater
    difficulty: The difficulty of the puzzle
    created_at: Creation timestamp
    category: Puzzle category/theme
    estimated_time: Estimated solve time in minutes

    """
    created_at: datetime
    category: Optional[str]
    estimate_time: Optional[int] = None
    title: str = "Untitled Crossword"
    author: str = "Tamman Montanaro"
    difficulty: Optional[int] = 1

    def __post_init__(self):
        if not 1 <= self.difficulty <= 5:
            raise ValueError("difficulty must be between 1 and 5")

@dataclass
class Puzzle:
    """
    Represents a complete puzzle.

    Attributes:
        grid: The puzzle grid
        words: The list of words in the puzzle
        metadata: The Puzzle metadata
    """

    grid: Grid
    words: List[CrosswordWord] = field(default_factory=list)
    metadata: PuzzleMetaData = field(default_factory=PuzzleMetaData)


    def add_word(self, word: CrosswordWord) -> None:
        """Add a word to the puzzle."""
        self.words.append(word)

    def get_word_by_number(self, number: int, direction: Direction) -> Optional[CrosswordWord]:
        """Get a word from the clue number and direction, None if doesn't exist"""
        for word in self.words:
            if number == word.number and direction == word.direction:
                return word
        return None

    def get_words_by_direction(self, direction: Direction) -> List[CrosswordWord]:
        """Return a list of the words based on the direction"""
        return [w for w in self.words if w.direction == direction]

    @property
    def accross_words(self) -> List[CrosswordWord]:
        """Return all the ACROSS words """
        return [w for w in self.words if w.direction == Direction.ACROSS]

    @property
    def down_words(self) -> List[CrosswordWord]:
        """Return all the DOWN words """
        return [w for w in self.words if w.direction == Direction.DOWN]

    def get_clues(self) -> Dict[str, List[Clue]]:
        """
        Return all the clues in a dictinoary organized by the directions
        """
        clues = {'ACROSS': [], 'DOWN': []}


        for word in sorted(self.words, key=lambda w: w.number or 0):
            if word.number:
                clue = Clue(
                    text = word.clue,
                    answer = word.text,
                    number = word.number,
                    direction = word.direction.value
                )
                clues[word.direction.value].append(clue)

        return clues

    def validate_structure(self) -> List[str]:
        """
        Validate the puzzle structure and return a list of errors
        Returns empty list if valid
        """

        errors = []

        """Check if puzzle has words"""
        if not self.words:
            errors.append("Puzzle has no words")

        """Check if all the words fit in the grid"""
        for word in self.words:
            if word.end_row >= self.grid.size:
                errors.append(f"Word '{word.text}' extends beyond the grid (rows)")
            if word.end_col >= self.grid.size:
                errors.append(f"Word '{word.text}' extends beyond the grid (cols)")

        """Check for overlapping words with different letters"""
        for i, word1 in enumerate(self.words):
            for word2 in self.words[i+1]:
                intersection = word1.intersects_with(word2)

                if intersection:
                    row, col = intersection

                    if word1.direction == Direction.ACROSS:
                        char1 = word1.text[col - word1.col]
                        char2 = word2.text[row - word2.row]
                    else:
                        char1 = word1.text[row - word1.row]
                        char2 = word2.text[col - word2.col]

                    if char1 != char2:
                        errors.append(
                            f"Invalid Intersection between '{word1.text}' and '{word2.text}' "
                            f"at ({row}, {col}): '{char1}' != '{char2}'"
                        )

        return errors

    def is_valid(self) -> bool:
        """Check to see if the puzzle structure is valid"""
        return len(self.validate_structure()) == 0

    def __repr__(self) -> str:
        return (f"Puzzle(title='{self.metadata.title}',"
                f"words='{self.words}', "
                f"size={self.grid.size} x {self.grid.size})")