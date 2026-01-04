"""Crossword data model representing a word in the puzzle"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Direction(Enum):
    """Direction of the crossword word placement in grid"""
    ACROSS = "ACROSS"
    DOWN = "DOWN"

    def is_horizontal(self):
        return self == Direction.ACROSS

    def is_vertical(self):
        return self == Direction.DOWN

@dataclass
class CrosswordWord:
    """
    Represents a word placed in the crossword puzzle

    Attributes:
        text: The word text (uppercase)
        clue: The clue for this word
        row: Starting row position (0-indexed)
        col: Starting col position (0-indexed)
        direction: Direction of the word (ACROSS or DOWN)
        number: Clue number (assigned during puzzle building)
    """
    text: str
    clue: str
    row: int
    col: int
    direction: Direction
    number: Optional[int] = None

    def __post_init__(self):
        """Validate and normalize the word data"""
        self.text = self.text.upper()
        if not self.text.isalpha():
            raise ValueError(f'{self.text} must contain only letters')
        if len(self.text) < 2:
            raise ValueError(f'{self.text} must contain exactly 3 characters')
        if self.row < 0 or self.col < 0:
            raise ValueError(f'Position cannot be negative: ({self.row}, {self.col})')

    @property
    def length(self) -> int:
        """Return the length of the word"""
        return len(self.text)

    @property
    def end_row(self) -> int:
        """Return the ending row position"""
        if self.direction == Direction.DOWN:
            return self.row + self.length - 1
        return self.row

    @property
    def end_col(self) -> int:
        """Return the ending column position"""
        if self.direction == Direction.ACROSS:
            return self.col + self.length - 1
        return self.col

    def get_char_at(self, index: int) -> str:
        """Return the character at a given index"""
        if 0 <= index < self.length:
            return self.text[index]
        raise IndexError(f"Index {index} out of range for word of length {self.length}")


    def get_position_at(self, index: int) -> tuple[int, int]:
        """Return the grid position  for character at index"""
        if self.direction == Direction.ACROSS:
            return self.row, self.col + index
        else:
            return self.row + index, self.col


    def contain_position(self, row: int, col: int) -> bool:
        """Check to see if the word occupies a given grid position"""
        if self.direction == Direction.ACROSS:
            return self.row == row and self.col <= col <= self.end_col
        else:
            return self.row <= row <= self.end_row and self.col == col

    def intersects_with(self, other: 'CrosswordWord') -> Optional[tuple[int, int]]:
        """Check to see if the word interesects with another word.
        Return the grid position of intersection if found, None otherwise"""
        if self.direction == other.direction:
            return None

        for i in range(self.length):
            pos = self.get_position_at(i)
            if other.contain_position(*pos):
                return pos

        return None


    def __repr__(self):
        return f'CrosswordWord({self.text}, {self.clue}, {self.direction.value}, pos=({self.row}, {self.col}), num={self.number})'

    def __eq__(self, other) -> bool:
        if not isinstance(other, CrosswordWord):
            return False

        return (
            self.text == other.text and
            self.clue == other.clue and
            self.row == other.row and
            self.col == other.col and
            self.direction == other.direction
        )

    def __hash__(self) -> int:
        return hash((self.text, self.clue, self.direction, self.row, self.col))
