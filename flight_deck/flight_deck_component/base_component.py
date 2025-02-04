from __future__ import annotations

from typing import List


class BaseComponent:

    __content: List[BaseComponent] = []

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

    def __init__(self, content: List[BaseComponent] | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.__content = content or []
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)

    def getContent(self) -> List[BaseComponent]:
        return self.__content

    def clearContent(self) -> BaseComponent:
        self.__content = []
        return self

    def addContents(self, components: List[BaseComponent]) -> BaseComponent:
        for component in components:
            self.addContent(component)

        return self

    def addContent(self, component: BaseComponent) -> BaseComponent:
        component.x += self.__x
        component.y += self.__y
        self.__content.append(component)
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
