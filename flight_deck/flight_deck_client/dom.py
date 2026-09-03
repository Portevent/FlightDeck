import curses
from typing import List

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

    # TODO : Should not use curses but rather Display agnostic values
    def onkey(self, char: int):
        if self.selectedIndex is None:
            return

        if char == 0xa:  # Enter key
            self.selected_component.enter()

        elif char == curses.KEY_LEFT:
            self.selected_component.goLeft()

        elif char == curses.KEY_RIGHT:
            self.selected_component.goRight()

        elif char == curses.KEY_UP:
            self.previous_component()

        elif char == curses.KEY_DOWN:
            self.next_component()

        elif char == curses.KEY_SR:  # Scroll ?up?
            pass
            # self.client.display.scroll(-1)

        elif char == curses.KEY_SF:  # Scroll ?down?
            pass
            # self.client.display.scroll(1)

        elif char == 8:  # Del key
            self.selected_component.delete()

        elif char == curses.KEY_DC:
            self.selected_component.suppr()

        else:
            self.selected_component.inputChar(chr(char))

            #TODO : Map key start and end