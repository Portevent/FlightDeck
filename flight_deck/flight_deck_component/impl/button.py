from typing import Callable

from flight_deck.flight_deck_component.component import Template, Input, ComponentName, Output
from flight_deck.flight_deck_component.interaction_component import InteractionComponent
from flight_deck.flight_deck_display.color import Color


@ComponentName("button")
@Input("text")
@Input("onClick")
@Output("buttonColor")
@Template("""
<Template>
    <text text="@formatted_text" color="#buttonColor"/>
</Template>
""")
class ButtonComponent(InteractionComponent):
    """
    Simple Button Component
    """
    text: str
    onClick: Callable
    buttonColor: Color

    def start(self):
        self.buttonColor = Color.CLASSIC

    @property
    def formatted_text(self):
        return f"[{self.text}]"


    def __onclick(self):
        self.onClick()

    def inputChar(self, char: str):
        pass

    def goLeft(self):
        pass

    def goRight(self):
        pass

    def goUp(self):
        self.client.dom.previous_component()

    def goDown(self):
        self.client.dom.next_component()

    def enter(self):
        self.__onclick()

    def goStart(self):
        pass

    def goEnd(self):
        pass

    def delete(self):
        pass

    def suppr(self):
        pass

    def displayCursor(self):
        self.move_cursor((0, 0), 0)

    def select(self):
        super().select()
        self.buttonColor = Color.SELECTED

    def unselect(self):
        super().unselect()
        self.buttonColor = Color.CLASSIC