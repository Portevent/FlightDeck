from __future__ import annotations

from typing import List


class BaseComponent:

    _contents: List[BaseComponent] = []

    # Position within component to place next component
    _next_content_x: int
    _next_content_y: int

    parent: BaseComponent | None = None

    __width: int

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, value: int):
        if self.width == value:
            return

        self.__width = value

        if self.parent:
            self.parent.updatePosition()

    __height: int

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, value: int):
        if self.height == value:
            return

        self.__height = value

        if self.parent:
            self.parent.updatePosition()

    __x: int

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        if self.x == value:
            return

        self.__x = value

        if self.parent:
            self.parent.updatePosition()

    __y: int
    
    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value: int):
        if self.y == value:
            return
        
        self.__y = value
        
        if self.parent:
            self.parent.updatePosition()

    def __init__(self, content: List[BaseComponent] | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 1, parent: BaseComponent | None = None):
        self._contents = content or []
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)
        self.parent = parent
        self._next_content_x = 0
        self._next_content_y = 0

    def getContent(self) -> List[BaseComponent]:
        return self._contents

    def clearContent(self) -> BaseComponent:
        self._contents = []
        return self

    def addContents(self, components: List[BaseComponent]) -> BaseComponent:
        for component in components:
            self.addContent(component)

        return self

    def addContent(self, component: BaseComponent) -> BaseComponent:
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
        self.displayBeforeContent()
        for content in self.getContent():
            content.display()
        self.displayAfterContent()

    def displayBeforeContent(self):
        pass

    def displayAfterContent(self):
        pass
