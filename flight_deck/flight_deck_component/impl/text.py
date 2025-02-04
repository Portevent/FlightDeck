from flight_deck.flight_deck_component.component import Input, Component, ComponentName


@ComponentName("text")
@Input("text")
class TextComponent(Component):

    text: str

    def start(self):
        lines = self.text.split("\n")
        self.height = len(lines)
        self.width = max(map(len, lines))

    def displayAfterContent(self):
        self._displayText(self.text, (0,0))
