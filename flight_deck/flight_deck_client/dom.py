import curses
from typing import List

from flight_deck.flight_deck_component.base_component import BaseComponent

class FlightDeckDom:
    # Index of the selected field
    selectedIndex: int | None = None

    topComponent: BaseComponent

    selectableComponents: List[BaseComponent]

    def __init__(self):
        self.topComponent = None
        self.selectableComponents = []
        self.selectedIndex = 0

    def setTopComponent(self, component: BaseComponent, selectableComponents: List[BaseComponent]):
        self.topComponent = component
        self.selectableComponents = selectableComponents
        self.selectComponent(0)

    @property
    def selected_component(self) -> BaseComponent:
        """
        Returns the selected Component
        :return: Component
        """
        return self.selectableComponents[self.selectedIndex]

    def selectComponent(self, index: int):
        """
        Set the selected component to given index
        :param index: Index of the Component
        """
        if self.selectedIndex is not None:
            self.selected_component.unselect()

        self.selectedIndex = index
        self.selected_component.select()

    def nextComponent(self):
        if self.selectedIndex < len(self.selectableComponents) - 1:
            self.selectComponent(self.selectedIndex + 1)

    def previousComponent(self):
        if self.selectedIndex > 0:
            self.selectComponent(self.selectedIndex - 1)

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
            self.previousComponent()

        elif char == curses.KEY_DOWN:
            self.nextComponent()

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