"""
Grid model representing the crossword grid structure
"""

from dataclasses import dataclass
from typing import List
from app.models.cell import Cell


@dataclass
class Grid:
    """
    Represents the crossword puzzle grid.

    Attributes:
        size: Dimension of the square grid
        cells: 2D array of Cell objects
    """

    def __init__(self, size: int):
        """Initialize an empty grid of given size"""
        if size < 5:
            raise ValueError("Grid size must be at least 5")
        self.size = size
        self.cells = List[List[str]] = [
            [Cell() for _ in range(size)] for _ in range(size)
        ]

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check to see if the given row and column are valid within the grid"""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty_at(self, row: int, col: int) -> bool:
        """Check to see if the given row and column are empty"""
        if self.is_valid_position(row, col):
            return self.cells[row][col].is_empty()

    def get_cell(self, row: int, col: int) -> Cell:
        """Return the Cell for a given row and column, None if not valid position"""
        if self.is_valid_position(row, col):
            return self.cells[row][col]
        return None

    def set_cell(self, row: int, col: int, cell: Cell) -> None:
        """Set the given cell for a given row and column, if valid position"""
        if self.is_valid_position(row, col):
            self.cells[row][col] = cell

    def clear_grid(self) -> None:
        """Clears the grid and reset the cells."""
        for row in self.cells:
            for cell in row:
                cell.clear()

    def get_row(self, row: int) -> List[Cell]:
        """Returns the row of the grid."""
        if not 0 <= row < self.size:
            raise ValueError("The Row must be within the grid size")
        return self.cells[row]

    def get_col(self, col: int) -> List[Cell]:
        """Returns the column of the grid."""
        if not 0 <= col < self.size:
            raise ValueError("The Column must be within the grid size")
        return [self.cells[row][col] for row in self.cells]

    def copy(self) -> 'Grid':
        """Create a deep copy of this grid"""
        new_grid = Grid(self.size)
        for i in range(self.size):
            for j in range(self.size):
                original_cell = self.cells[i][j]
                new_grid.cells[i][j] = Cell(
                    letter=original_cell.letter,
                    cell_type=original_cell.cell_type,
                    number=original_cell.number,
                    is_start_across=original_cell.is_start_across,
                    is_start_down=original_cell.is_start_down
                )
        return new_grid

    def __repr__(self) -> str:
        """String representation of the grid"""
        lines = []
        for row in self.cells:
            lines.append(" ".join(str(cell) for cell in row))
        return "\n".join(lines)


    def to_2d_list(self) -> List[List[str]]:
        """Convert grid to a 2D list of letters"""
        return [[cell.letter or '' for cell in row] for row in self.cells]










