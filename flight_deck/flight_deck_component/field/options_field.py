from typing import List

from flight_deck.elements.element import SetValidChar
from flight_deck.elements.visual_field import VisualField, HideCursor


@SetValidChar("")
@HideCursor
class OptionsField(VisualField):
    """
    Simple option field, where its value can be selected with left and right keys
    """

    values: List[str]
    values_count: int
    _index: int

    loop: bool

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int):
        if index >= self.values_count:
            index = 0 if self.loop else (self.values_count - 1)

        if index < 0:
            index = (self.values_count - 1) if self.loop else 0

        self._index = index
        self.value = self.values[self._index]

    def __init__(self, values: List[str], x: int = 0, y: int = 0, width: int | None = None, height: int | None = None,
                 name: str = "", label: str | None = None, loop: bool = True, index: int = 0):

        self.loop = loop
        self.values = values
        self.values_count = len(self.values)
        self._index = index

        super().__init__(x, y, width, height, name, label, values[index],
                         valueBackgroundSize=max(len(x) for x in values) + 4)

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        self.index -= 1

    def goRight(self):
        self.index += 1

    def enter(self):
        pass

    def start(self):
        if self.index > 0:
            self.index = 0

    def end(self):
        if self.index < self.values_count - 1:
            self.index = self.values_count - 1

    def delete(self):
        pass

    def suppr(self):
        pass

    def _generateValueBackground(self, size: int):
        return " " * size

    @property
    def formatedValue(self) -> str:
        return f"{'<' if self.loop or self.index > 0 else ' '} {self.value} {'>' if self.loop or self.index < (self.values_count - 1) else ' '}"
