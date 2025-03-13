from __future__ import annotations

from typing import List, Tuple, Type, Dict, Callable
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
            return self._inputs.get(name, None)

        def setInput(self, value):
            if self._inputs.get(name) == value:
                return
            self.updateInput(name, value)

        setattr(cls, name, property(getInput, setInput))
        return cls

    return addProperty


def Output(name: str):
    """
    Add Output to a component
    :param name: Output name to bind to
    """

    def addProperty(cls: Type[Component]):
        def getOutput(self):
            return self._outputs[name]

        def setOutput(self, value):
            if self._outputs.get(name) == value:
                return
            self._outputs[name] = value
            self.onOutputChange(name, value)

        setattr(cls, name, property(getOutput, setOutput))
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
    _outputs: Dict[str, any]
    _outputsObersvers: Dict[str, List[Callable]]

    client: FlightDeckBaseClient

    id: str

    def __init__(self, client: FlightDeckBaseClient, inputs: Dict[str, any] | None = None,
                 binds: List[Tuple[Component, str, str]] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self._display = client.display
        self._inputs = inputs or {}
        self._outputs = {}
        self._outputsObersvers = {}
        if binds:
            for page, input, bind in binds:
                def updateInput(value):
                    self.updateInput(input, value)

                page.addOutputListener(bind, updateInput)

        self.start()

    def start(self):
        pass

    @classmethod
    def getComponentName(cls) -> str:
        return cls._flight_deck_component_name

    def addOutputListener(self, output: str, callable: Callable):
        if output not in self._outputsObersvers:
            self._outputsObersvers[output] = []

        self._outputsObersvers[output].append(callable)

    def onOutputChange(self, output: str, value):
        for observer in self._outputsObersvers.get(output, []):
            observer(value)

    def updateInput(self, input: str, value: any):
        self._inputs[input] = value
        self.onInputChange(input, value)

    def _displayText(self, text: List[str] | str, position: Tuple[int, int] = (0, 0), color: Color = Color.CLASSIC):
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

    def onInputChange(self, input: str, value: str):
        """
        Called when an input is updated
        :param input: Name of updated input
        :param value: New value
        """
        self.display()

    def iterOverChildren(self):
        for component in self.getContent:
            yield component
            component.iterOverChildren()

    def searchChildren(self, id: str) -> Component:
        for component in self.iterOverChildren():
            if component.id == id:
                return component

        return None
