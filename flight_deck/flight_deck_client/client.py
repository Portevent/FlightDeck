from typing import Type

from flight_deck.flight_deck_client.base_client import FlightDeckBaseClient
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

    def __init__(self, display: FlightDeckDisplay | None = None):
        super().__init__(display)
        self.addComponent(TextComponent)
        self.addComponent(ButtonComponent)
        self.addComponent(Logo)
        self.addComponent(Break)
        self.addComponent(Horizontal)
        self.addComponent(TextField)
        self.addComponent(OptionsField)
        self.addComponent(DateField)

    def addComponent(self, component: Type[Component]):
        if not hasattr(component, '_flight_deck_component_name'):
            raise FlightDeckGivenIncorrectComponentException(
                f"FlightDeck can't register {component} as it is not a proper Component")

        if component.getComponentName() in self.components:
            raise FlightDeckAlreadyHasComponentException(
                f"FlightDeck already contains a component for <{component.getComponentName()}>")

        self.components[component.getComponentName()] = component

    def setRoutes(self, routes):
        """
        Set routes for this flight deck.
        :param routes: Map of string key to Component classes
        """
        self.routes = routes

    def addRoute(self, name: str, page: Type[Component]):
        """
        Add a route for a given name to a Component class.
        :param name: Route name
        :param page: Route component
        """
        self.routes[name] = page

    def navigateTo(self, name: str):
        self.dom.setTopComponent(*ComponentBuilder.instantiate(self.routes[name], self))
        self.dom.topComponent.display()

    def start(self, defaultPage: str | None = None):
        if defaultPage:
            self.navigateTo(defaultPage)

        self.display.start_listening(self.onkey)

    def onkey(self, key: str):
        if self.dom:
            self.dom.onkey(key)
