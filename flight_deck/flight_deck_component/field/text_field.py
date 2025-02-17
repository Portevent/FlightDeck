from flight_deck.flight_deck_component.component import Input
from flight_deck.flight_deck_component.field.field import Field

@Input("insertMode")
@Input("maxSize")
class TextField(Field):
    """
    Simple text field that user can type value into
    """

    insertMode: bool
    _cursorPosition: int = 0

    def start(self):
        # Todo : create default values for input
        if self.insertMode is None:
            self.insertMode = False
        if self.maxSize is None:
            self.maxSize = 15
        super().start()

    @property
    def cursorPosition(self) -> int:
        return self._cursorPosition

    @cursorPosition.setter
    def cursorPosition(self, index: int):
        if index > self.current_size:
            index = self.current_size

        if index < 0:
            index = 0

        if self._cursorPosition == index:
            return

        self._cursorPosition = index

    def getValueMaxSize(self) -> int:
        return self.maxSize

    def inputChar(self, char: str):
        # If we reached max size, we don't add more character
        if self.maxSize and self.current_size >= self.maxSize:
            # Except in insert mode (when we just replace char)
            if not (self.insertMode and self.cursorPosition < self.current_size):
                return

        self.value = self.value[:self.cursorPosition] + char + self.value[self.cursorPosition + (1 if self.insertMode else 0):]
        self.cursorPosition += 1

    def goLeft(self):
        self.cursorPosition -= 1

    def goRight(self):
        self.cursorPosition += 1

    def enter(self):
        # TODO : self.page.next()
        pass

    def goStart(self):
        self.cursorPosition = 0

    def goEnd(self):
        self.cursorPosition = self.current_size

    def delete(self):
        if self.cursorPosition > 0:
            self.value = self.value[:self.cursorPosition-1] + self.value[self.cursorPosition:]
            self.cursorPosition -= 1

    def suppr(self):
        if self.cursorPosition < self.current_size:
            self.value = self.value[:self.cursorPosition] + self.value[self.cursorPosition+1:]
            self.cursorPosition += 0

    def updateValue(self):
        self.current_size = len(self.value)
        self.formatedValue = self.textOver(self.value, self.value_fill, self.maxSize)
        self.displayCursor()

    def displayCursor(self):
        self._moveCursor((0, self.cursorPosition)) # TODO : Check if x and y are not confused