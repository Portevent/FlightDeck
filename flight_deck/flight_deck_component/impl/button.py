from typing import Callable


from flight_deck.flight_deck_component.component import Template, Component, Input, ComponentName
from flight_deck.flight_deck_component.interaction_component import InteractionComponent


@ComponentName("button")
@Input("text")
@Input("onClick")
@Template("""
<Template>
    <text text="@formatted_text"/>
</Template>
""")
class ButtonComponent(InteractionComponent):

    text: str
    onClick: Callable

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
        self.client.dom.previousComponent()

    def goDown(self):
        self.client.dom.nextComponent()

    def enter(self):
        self.__onclick()

    def start(self):
        pass

    def end(self):
        pass

    def delete(self):
        pass

    def suppr(self):
        pass

    def select(self):
        pass

    def unselect(self):
        pass