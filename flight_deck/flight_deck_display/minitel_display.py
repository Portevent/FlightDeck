
from collections.abc import Callable

from miniminitel import MiniMinitel, MinitelInput, MinitelCode

from flight_deck import FlightKey
from flight_deck.flight_deck_display.color import Color
from flight_deck.flight_deck_display.display import FlightDeckDisplay, Position


class FlightDeckMinitelDisplay(FlightDeckDisplay):
    """
    Simple Minitel terminal that display windows
    """
    width: int
    height: int
    message_count: int = 1
    prompt_cursor: int = 0

    # Text variation for each color
    color_variation: dict[Color, int]

    minitel: MiniMinitel

    listening: bool  # Break bool for listening user input

    def __init__(self, port: str = "COM4"):
        """
        Init the windows
        :param client:
        """

        self.minitel = MiniMinitel(port)
        self.listening = False

    def displayText(self, text: str, position: Position, color: Color, refresh: bool = True):
        """
        Display text at position
        :param text: Text to display
        :param height: Position (vertical)
        :param start: Start position (horizontal)
        :param color: Text variation
        """
        self.moveCursor(position)
        self.minitel.write(text)

    def moveCursor(self, position: Position, cursorType: int | None = None, refresh: bool = True):
        """
        Move cursor
        :param x: x position
        :param y: y position
        """

        if cursorType is not None:
            self.setCursor(cursorType)

        self.minitel.cursor_move_to(position[0] + 1, position[1] + 1)

    def setCursor(self, cursor_type: int):
        if cursor_type > 0:
            self.minitel.cursor_on()
        else:
            self.minitel.cursor_off()

    def __enter__(self):
        self.minitel.__enter__()
        self.minitel.set_non_blinking()
        self.minitel.set_grandeur_normale()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.minitel.__exit__(exc_type, exc_val, exc_tb)
        pass

    def start_listening(self, onkey: Callable):
        """
        Start listening to user input
        """
        self.listening = True
        self.minitel.start_listening(self.convert_minitel_input_to_flightdeck(onkey))

    def convert_minitel_input_to_flightdeck(self, onkey: Callable):
        def recieve(input: MinitelInput):
            key = None

            if input.code == MinitelCode.TEXT:
                key = FlightKey.text(input.text)

            elif input.code == MinitelCode.CARRIAGE_RETURN:
                key = FlightKey.special("Enter")

            elif input.code == MinitelCode.MOVE_LEFT:
                key = FlightKey.special("Left")

            elif input.code == MinitelCode.MOVE_RIGHT:
                key = FlightKey.special("Right")

            elif input.code == MinitelCode.MOVE_UP:
                key = FlightKey.special("Up")

            elif input.code == MinitelCode.MOVE_DOWN:
                key = FlightKey.special("Down")

            elif input.code == MinitelCode.DELETE:  # Del key
                key = FlightKey.special("Delete")

            if key is not None:
                onkey(key)

        return recieve

    def clear(self):
        self.minitel.clear_screen()
