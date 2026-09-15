from typing import List

from flight_deck.flight_deck_client.keys import FlightKey
from flight_deck.flight_deck_component.base_component import BaseComponent
from flight_deck.flight_deck_component.interaction_component import InteractionComponent


class FlightDeckDom:
    # Index of the selected field
    selectedIndex: int | None = None
    selected_component: InteractionComponent | None = None

    topComponent: BaseComponent | None = None

    selectableComponents: List[InteractionComponent]

    def __init__(self):
        self.topComponent = None
        self.selectableComponents = []
        self.selectedIndex = 0

    def set_top_component(self, component: BaseComponent, selectable_components: List[InteractionComponent]):
        self.topComponent = component
        self.selectableComponents = selectable_components
        self.select_component(0)

    def select_component(self, index: int):
        """
        Set the selected component to given index
        :param index: Index of the Component
        """
        if self.selected_component is not None:
            self.selected_component.unselect()

        self.selectedIndex = index
        self.selected_component = self.selectableComponents[index]
        self.selected_component.select()

    def next_component(self):
        if self.selectedIndex < len(self.selectableComponents) - 1:
            self.select_component(self.selectedIndex + 1)

    def previous_component(self):
        if self.selectedIndex > 0:
            self.select_component(self.selectedIndex - 1)

    def onkey(self, key: FlightKey):
        if self.selectedIndex is None:
            return
        
        if not key.special:
            self.selected_component.inputChar(key.key)
            return
        
        if key.key == "Enter":  # Enter key
            self.selected_component.enter()

        elif key.key == "Left":
            self.selected_component.goLeft()

        elif key.key == "Right":
            self.selected_component.goRight()

        elif key.key == "Up":
            self.previous_component()

        elif key.key == "Down":
            self.next_component()

        elif key.key == "Delete":  # Del key
            self.selected_component.delete()

        elif key.key == "Suppr":
            self.selected_component.suppr()

