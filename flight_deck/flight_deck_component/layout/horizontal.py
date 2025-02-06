from flight_deck.flight_deck_component.base_component import BaseComponent
from flight_deck.flight_deck_component.component import Component, ComponentName


@ComponentName("horizontal")
class Horizontal(Component):
    """
    Display element horizontally.
    """

    def addContent(self, component: BaseComponent) -> BaseComponent:
        component.x += self.x
        component.x += self._next_content_x
        component.y += self.y
        component.y += self._next_content_y
        self._next_content_x += component.width
        self._next_content_y = 0
        self.width += component.width
        # Purposeless as height hot update isn't supported yet
        self.height = max(component.height, self.height)
        self._contents.append(component)
        return self