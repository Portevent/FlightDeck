from typing import override


@SetValidChar(chars="0123456789")
class DateField(TextField):
    """
    Simple Date field
    """

    def start(self):
        super().start()
        self.maxSize = 6
        self.insertMode = False

    def getValueMaxSize(self) -> int:
        return 6

    def updateValue(self):
        self.current_size = len(self.value)
        self.formatedValue =  f"{TextFormater.override(str(self.value)[0:2], '  ')}.
                                {TextFormater.override(str(self.value)[2:4], '  ')}.
                                {TextFormater.override(str(self.value)[4:8], '    ')}"
        self.displayCursor()

    def displayCursor(self):
        self._moveCursor((0, self.cursorPosition + 2 if self.cursorPosition > 4 else (1 if self.cursorPosition > 2 else 0))) # TODO : Check if x and y are not confused