from abc import abstractmethod
from typing import Dict, Type

from flight_deck.flight_deck_client.dom import FlightDeckDom
from flight_deck.flight_deck_component.base_component import BaseComponent
from flight_deck.flight_deck_display.display import FlightDeckDisplay


class FlightDeckBaseClient:
    display: FlightDeckDisplay | None

    routes: Dict[str, Type[BaseComponent]]
    components: Dict[str, Type[BaseComponent]]

    dom: FlightDeckDom

    def __init__(self, display: FlightDeckDisplay | None = None):
        self.display = display
        self.components = {}
        self.routes = {}
        self.dom = FlightDeckDom()

    def getComponent(self, name: str) -> Type[BaseComponent]:
        if not name in self.components:
            raise Exception(f"FlightDeck doesn't know component {name}")

        return self.components[name]

    def __enter__(self):
        if self.display is None:
            raise Exception("Entering Client without specifying a display")

        self.display.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.display.__exit__(exc_type, exc_val, exc_tb)


    def setDisplay(self, display: FlightDeckDisplay):
        """
        Set the display
        :param display: New display
        """
        self.display = display
        return self

    @abstractmethod
    def start(self, defaultPage: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def onkey(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def navigateTo(self, name: str):
        raise NotImplementedError