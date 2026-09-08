from typing import Type, Dict

from flight_deck.flight_deck_client.base_client import FlightDeckBaseClient
from flight_deck.flight_deck_client.dom import FlightDeckDom
from flight_deck.flight_deck_component.base_component import BaseComponent
from flight_deck.flight_deck_component.field import TextField, OptionsField, DateField
from flight_deck.flight_deck_component.impl import Logo, Break
from flight_deck.flight_deck_component.impl.button import ButtonComponent
from flight_deck.flight_deck_component.component import Component
from flight_deck.flight_deck_component.component_builder import ComponentBuilder
from flight_deck.flight_deck_component.impl.text import TextComponent
from flight_deck.flight_deck_component.layout.horizontal import Horizontal
from flight_deck.flight_deck_display.display import FlightDeckDisplay
from flight_deck.flight_deck_exceptions.client import FlightDeckGivenIncorrectComponentException, \
    FlightDeckAlreadyHasComponentException


class FlightDeck(FlightDeckBaseClient):
    dom: FlightDeckDom

    def __init__(self, display: FlightDeckDisplay | None = None):
        super().__init__(display)
        self.add_component(TextComponent)
        self.add_component(ButtonComponent)
        self.add_component(Logo)
        self.add_component(Break)
        self.add_component(Horizontal)
        self.add_component(TextField)
        self.add_component(OptionsField)
        self.add_component(DateField)
        self.dom = FlightDeckDom()

    def add_component(self, component: Type[Component]):
        if not hasattr(component, '_flight_deck_component_name'):
            raise FlightDeckGivenIncorrectComponentException(
                f"FlightDeck can't register {component} as it is not a proper Component")

        if component.getComponentName() in self.components:
            raise FlightDeckAlreadyHasComponentException(
                f"FlightDeck already contains a component for <{component.getComponentName()}>")

        self.components[component.getComponentName()] = component

    def set_routes(self, routes: Dict[str, Type[BaseComponent]]):
        """
        Set routes for this flight deck.
        :param routes: Map of string key to Component classes
        """
        self.routes = routes

    def add_route(self, name: str, page: Type[Component]):
        """
        Add a route for a given name to a Component class.
        :param name: Route name
        :param page: Route component
        """
        self.routes[name] = page

    def navigate_to(self, name: str):
        self.dom.set_top_component(*ComponentBuilder.instantiate(self.routes[name], self))
        self.display.clear()
        self.dom.topComponent.display()
        self.dom.select_component(0)

    def start(self, default_page: str | None = None):
        if default_page:
            self.navigate_to(default_page)

        self.display.start_listening(self.onkey)

    def onkey(self, key: str):
        if self.dom:
            self.dom.onkey(key)
