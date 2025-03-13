import curses, curses.panel
from collections.abc import Callable

from flight_deck.flight_deck_display.color import Color
from flight_deck.flight_deck_display.display import FlightDeckDisplay, Position


class FlightDeckCursesDisplay(FlightDeckDisplay):
    """
    Simple curses terminal that display windows
    """
    width: int
    height: int
    message_count: int = 1
    prompt_cursor: int = 0

    # Text variation for each color
    color_variation: dict[Color, int]

    input_windows: "_CursesWindow"

    listening: bool  # Break bool for listening user input

    def __init__(self):
        """
        Init the windows
        :param client:
        """

        self.stdscr = curses.initscr()
        self.input_windows = self.stdscr
        curses.noecho()
        curses.cbreak()

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(Color.CLASSIC, curses.COLOR_WHITE, -1)
            curses.init_pair(Color.PROMPT, curses.COLOR_BLUE, -1)
            curses.init_pair(Color.SUCCESS, curses.COLOR_GREEN, -1)
            curses.init_pair(Color.ERROR, curses.COLOR_RED, -1)
            curses.init_pair(Color.DEBUG, curses.COLOR_YELLOW, -1)
            curses.init_pair(Color.LOG, curses.COLOR_WHITE, -1)

        self.color_variation = {Color.CLASSIC: 0,
                                Color.PROMPT: 0, Color.SUCCESS: curses.A_BOLD,
                                Color.DEBUG: 0, Color.ERROR: curses.A_BOLD,
                                Color.LOG: curses.A_ITALIC}

        self.stdscr.keypad(True)
        # self.stdscr.leaveok(True)
        curses.curs_set(1)
        self.width = curses.COLS
        self.height = curses.LINES
        self.listening = False

    def displayText(self, text: str, position: Position, color: Color, refresh: bool = True):
        """
        Display text at position
        :param text: Text to display
        :param height: Position (vertical)
        :param start: Start position (horizontal)
        :param color: Text variation
        :param refresh: Refresh window
        """
        self.stdscr.addstr(position[1], position[0], text,
                           curses.color_pair(color) if isinstance(color, int) else self.color_variation[color])
        if refresh:
            self._refresh()

    def moveCursor(self, position: Position, cursorType = None, refresh: bool = True):
        """
        Move cursor
        :param x: x position
        :param y: y position
        """
        self.input_windows.move(position[1], position[0])
        if refresh:
            self._refresh()

    def setCursor(self, cursor_type: int):
        curses.curs_set(cursor_type)

    def _refresh(self):
        self.stdscr.refresh()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(False)
        curses.endwin()
        exit()

    def start_listening(self, onkey: Callable):
        """
        Start listening to user input
        """
        self.listening = True
        while self.listening:
            char: int = self.input_windows.getch()

            if char == -1:
                pass
            else:
                onkey(char)

    def clear(self):
        self.input_windows.clear()
