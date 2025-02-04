from __future__ import annotations

from typing import List, Tuple, Type, Dict
from xml.etree import ElementTree
from xml.dom.minidom import Element

from flight_deck.flight_deck_client.base_client import FlightDeckBaseClient
from flight_deck.flight_deck_component.base_component import BaseComponent
from flight_deck.flight_deck_display.color import Color
from flight_deck.flight_deck_display.display import FlightDeckDisplay

def Input(name: str):
    """
    Add Input to a component
    :param name: Input name to bind to
    """

    def addProperty(cls: Type[Component]):

        def getInput(self):
            return self._inputs[name]

        def setInput(self, value):
            if self._inputs[name] == value:
                return
            self._inputs[name] = value
            self.onInputChange(name, value)

        setattr(cls, name, property(getInput, setInput))
        return cls

    return addProperty


def Template(template: str):
    """
    Set the Template of a component
    :param template:
    """

    def setTemplate(cls: Type[Component]):
        cls._flight_deck_template = ElementTree.fromstring(template)
        return cls

    return setTemplate


def ComponentName(name: str):

    def setName(cls: Type[Component]):
        cls._flight_deck_component_name = name
        return cls

    return setName

@Input("id")
class Component(BaseComponent):
    _flight_deck_component_name: str = "UNDEFINED"

    _display: FlightDeckDisplay | None

    _flight_deck_template: Element | None = None

    _inputs: Dict[str, any]

    client: FlightDeckBaseClient

    id: str

    def __init__(self, client: FlightDeckBaseClient, inputs: Dict[str, any] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self._display = client.display
        self._inputs = inputs or {}
        self.start()

    def start(self):
        pass

    def _displayText(self, text: List[str] | str, position: Tuple[int, int] = (0,0), color: Color = Color.CLASSIC):
        """
        Display text within the bounds of the component
        :param text: String to display (or multiple lines)
        :param position: Where to display the text
        :param color:
        """
        if self._display is None:
            return

        for y, line in enumerate(text if isinstance(text, List) else [text], start=position[1]):

            # Outside the box
            if y >= self.height or y < 0:
                continue

            for x, char in enumerate(line, start=position[0]):
                if x >= self.width or x < 0:
                    continue
                self._display.displayText(char, (self.x + x, self.y + y), color=color)

    def _moveCursor(self, position: Tuple[int, int], cursorType: int | None = None):
        """
        Move the cursor
        :param position:
        :param cursorType:
        """
        if self._display is None:
            return

        x = max(0, min(self.width, position[0]))
        y = max(0, min(self.height, position[1]))

        self._display.moveCursor((self.x + x, self.y + y), cursorType=cursorType)

    def setDisplay(self, display: FlightDeckDisplay) -> Component:
        """
        Set the display to use
        :param display:
        """
        self._display = display
        return self

    def onInputChange(self, input: str, name: str):
        """
        Called when an input is updated
        :param input: Name of updated input
        :param name: New value
        """
        self.display()

    def searchChildren(self, id: str) -> Component:
        for component in self.getContent():
            if component.id == id:
                return component

        return None