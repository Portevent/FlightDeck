from __future__ import annotations

from typing import List

from flight_deck.flight_deck_component.xy_component import XyComponent


class BaseComponent(XyComponent):
    """
    Base Component Class
    """
    _contents: List[BaseComponent] = []

    # Position within component to place next component
    _next_content_x: int
    _next_content_y: int

    parent: BaseComponent | None = None

    _width: int

    _height: int

    _x: int

    _y: int

    def __init__(self, content: List[BaseComponent] | None = None,
                 x: int = 0, y: int = 0, width: int = 0,
                 height: int = 1, parent: BaseComponent | None = None):
        super().__init__(x, y, width, height, parent)
        self._contents = content or []
        self._next_content_x = 0
        self._next_content_y = 0

    def getContent(self) -> List[BaseComponent]:
        """
        Get all content
        :return: List of Components
        """
        return self._contents

    def clearContent(self) -> BaseComponent:
        """
        Remove all content from this component
        :return: Self
        """
        self._contents = []
        return self

    def addContents(self, components: List[BaseComponent]) -> BaseComponent:
        """
        Add Components after the other content
        :param component: New children
        """
        for component in components:
            self.addContent(component)

        return self

    def addContent(self, component: BaseComponent) -> BaseComponent:
        """
        Add Component after the other content
        :param component: New child
        """
        component.x += self.x
        component.x += self._next_content_x
        component.y += self.y
        component.y += self._next_content_y
        self._next_content_y += component.height
        self._next_content_x = 0
        self.height += component.height
        # Purposeless as width hot update isn't supported yet
        self.width = max(component.width, self.width)
        self._contents.append(component)
        return self

    def updatePosition(self):
        self.display()

    def display(self):
        """
        Display the component
        :return:
        """
        self.displayBeforeContent()
        for content in self.getContent():
            content.display()
        self.displayAfterContent()

    def displayBeforeContent(self):
        """
        Display something before displaying the childs content
        """
        pass

    def displayAfterContent(self):
        """
        Display something after displaying the childs content
        """
        pass
