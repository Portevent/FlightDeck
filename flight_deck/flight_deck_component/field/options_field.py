from typing import List

from flight_deck.elements.element import SetValidChar
from flight_deck.elements.visual_field import VisualField, HideCursor


@SetValidChar("")
@HideCursor
@Input("loop")
@Input("values")
class OptionsField(Field):
    """
    Simple option field, where its value can be selected with left and right keys
    """

    values: List[str]
    values_count: int
    _index: int = 0

    # "= False" wouldn't work as @Input("loop") will override this. TODO : Default value for Input
    loop: bool = False

    def start(self):
        super().start()
        self.values_count = len(self.values)
        if self.loop is None: # TODO : Remove when default value for Input work
            self.loop = False

    def onInputChange(self, input: str, value: str):
        match input:
            case "values":
                self.values_count = len(self.values)
                self.index = self.index # Check if index still in range
            case _:
                super().onInputChange(input, value)
        
    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int):
        if index >= self.values_count:
            index = 0 if self.loop else (self.values_count - 1)

        if index < 0:
            index = (self.values_count - 1) if self.loop else 0

        if self._index == index:
            return

        self._index = index
        self.value = self.values[self._index]

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        self.index -= 1

    def goRight(self):
        self.index += 1

    def enter(self):
        pass

    def goStart(self):
        self.index = 0

    def goEnd(self):
        self.index = self.values_count - 1

    def delete(self):
        pass

    def suppr(self):
        pass

    def getValueMaxSize(self) -> int:
        return max(map(len, self.values))


    def updateValue(self):
        """
        Update the displayed label
        """
        rawFormatedValue = self.textOver(self.value, self.value_fill, self.value_max_size)
        self.formatedValue = f"{'<' if self.loop or self.index > 0 else ' '} {self.value} {'>' if self.loop or self.index < (self.values_count - 1) else ' '}"
