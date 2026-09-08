from flight_deck.flight_deck_component.component import Input, Component, ComponentName
from flight_deck.flight_deck_display.color import Color


@ComponentName("text")
@Input("text")
@Input("color")
class TextComponent(Component):

    text: str
    color: Color

    def start(self):
        lines = self.text.split("\n")
        self.height = len(lines)
        self.width = int(self._inputs.get("width") or max(map(len, lines)))

    def display_after_content(self):
        self._displayText(self.text, (0,0), color=self.color or Color.CLASSIC)
