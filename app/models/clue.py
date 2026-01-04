"""
Clue Model representing the crossword clues
"""
from dataclasses import dataclass
from typing import Optional
from word import Direction

@dataclass
class Clue:
    """
    Represents a crossword clue

    Attributes:
        text: The clue text
        answer: The answer to the clue (word)
        number: Clue number in the puzzle
        direction: direction of the answer (Direction enum)
        difficulty: Optional difficult rating (1-5)
        category: Optional category/topic
    """
    text: str
    answer: str
    number: int
    direction: Direction
    difficulty: Optional[int] = None
    category: Optional[str] = None


    def __post_init__(self):
        """Validate the clue data"""
        self.text = self.text.upper()
        self.answer = self.answer.upper().strip()
        if not self.text:
            raise ValueError("Clue text cannot be empty")
        if not self.answer:
            raise ValueError("Clue answer cannot be empty")
        if self.difficulty and not 1 <= self.difficulty <= 5:
            raise ValueError("Clue difficulty must be between 1 and 5")


    def matches_answer(self, answer: str) -> bool:
        """Check if the user answer matches the clue answer"""
        return answer.upper() == self.answer


    def __repr__(self):
        return f"Clue({self.number} {self.direction}: {self.text} --> {self.answer})"