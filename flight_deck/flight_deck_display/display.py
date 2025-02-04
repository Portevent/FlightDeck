from abc import ABC, abstractmethod
from typing import Tuple, Callable

from flight_deck.flight_deck_display.color import Color

Position = Tuple[int, int]

class FlightDeckDisplay(ABC):

    @abstractmethod
    def displayText(self, text: str, position: Position, color: Color):
        """
        Display text at position, with given color
        :param text:
        :param position:
        :param color:
        """
        raise NotImplementedError

    @abstractmethod
    def moveCursor(self, position: Position, cursorType: int | None = None):
        """
        Move cursor to position, and change its type if specified
        :param position: Position of the cursor
        :param cursorType: If specified, change cursor type
        """
        raise NotImplementedError

    @abstractmethod
    def setCursor(self, cursor_type: int):
        """
        Set cursor
        :param cursor_type: 1 for visible, 0 for invisible
        """
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    def start_listening(self, onkey: Callable):
        """
        Start listening to user input
        :param onkey: callback
        """
        raise NotImplementedError
