from flight_deck.flight_deck_component.component import Input
from flight_deck.flight_deck_component.field.field import Field

@Input("insertMode")
class TextField(Field):
    """
    Simple text field that user can type value into
    """

    insertMode: bool

    def start(self):
        # Todo : create default values for input
        if self.insertMode is None:
            self.insertMode = False

    def inputChar(self, char: str):
        # If we reached max size, we don't add more character
        if self.max_size and self.current_size >= self.max_size:
            # Except in insert mode (when we just replace char)
            if not (self.insertMode and self.cursorPosition < self.current_size):
                return

        self.value = self.value[:self.cursorPosition] + char + self.value[self.cursorPosition + (1 if self.insertMode else 0):]
        self.cursorPosition += 1

    def goLeft(self):
        if self.cursorPosition > 0:
            self.cursorPosition -= 1

    def goRight(self):
        if self.cursorPosition < self.current_size:
            self.cursorPosition += 1

    def enter(self):
        # TODO : self.page.next()
        pass

    def start(self):
        if self.cursorPosition > 0:
            self.cursorPosition = 0

    def end(self):
        if self.cursorPosition < self.current_size:
            self.cursorPosition = self.current_size

    def delete(self):
        if self.cursorPosition > 0:
            self.value = self.value[:self.cursorPosition-1] + self.value[self.cursorPosition:]
            self.cursorPosition -= 1

    def suppr(self):
        if self.cursorPosition < self.current_size:
            self.value = self.value[:self.cursorPosition] + self.value[self.cursorPosition+1:]
            self.cursorPosition += 0

    @property
    def formatedValue(self) -> str:
        return str(self.value)
