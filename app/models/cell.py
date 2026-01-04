"""Cell model representing """

from dataclasses import dataclass
from enum import Enum
from typing import Optional

"""The Cell Type is limited to two Enum Types."""
class CellType(Enum):
    """The type of the cell within the grid."""
    EMPTY = "EMTPY"
    LETTER = "LETTER"



@dataclass
class Cell:

    """ Represents a single cell withing the crossword grid.

    Attributes:
        letter: The letter within the cell represented by an Optional[str] type (str or None)
        cell_type: The type of the cell within the grid (EMPTY or LETTER)
        number: The number of the word tied to the cell (int or None)
        is_start_across: True or False depending on whether the cell contains the starting letter or not
        is_start_down: True or False depending on whether the cell contains the starting letter or not

    """
    letter: Optional[str] = None
    cell_type: CellType = CellType.EMPTY
    number: Optional[int] = None
    is_start_across: bool = False
    is_start_down: bool = False

    def is_empty(self) -> bool:
        """Returns True if the cell is empty, False otherwise. """
        return self.type == CellType.EMPTY

    def is_letter(self) -> bool:
        """Returns True if the cell is letter, False otherwise. """
        return self.type == CellType.LETTER

    def is_start_position(self) -> bool:
        """Returns True if the cell is starting position, False otherwise. """
        return self.is_start_across or self.is_start_down

    def set_letter(self, letter: str) -> None:
        """Sets the letter of the cell within the grid."""
        if letter:
            self.letter = letter.upper()
            self.cell_type = CellType.LETTER

    def get_letter(self) -> Optional[str]:
        """Returns the letter of the cell within the grid."""
        return self.letter

    def clear(self) -> None:
        """Clears the cell within the grid."""
        self.letter: Optional[str] = None
        self.cell_type: CellType = CellType.EMPTY
        self.number: Optional[int] = None
        self.is_start_across: bool = False
        self.is_start_down: bool = False

    def __repr__(self):
        """Returns a string representation of the cell within the grid."""
        if self.is_empty():
            return "■"
        return self.letter or "_"