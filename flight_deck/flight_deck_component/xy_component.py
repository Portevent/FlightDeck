from __future__ import annotations

from abc import ABCMeta, abstractmethod


class XyComponent(metaclass=ABCMeta):
    """
    Simple component with 2D coordinates and size
    """
    def __init__(self, x: int = 0, y: int = 0, width: int = 0,
                 height: int = 1, parent: XyComponent | None = None):
        self._height = int(height)
        self._width = int(width)
        self._y = int(y)
        self._x = int(x)
        self.parent = parent

    @abstractmethod
    def updatePosition(self):
        """
        Update the position of the component
        """
        pass

    @property
    def x(self) -> int:
        """
        X coordinates
        :return: Integer
        """
        return self._x

    @x.setter
    def x(self, value: int):
        """
        Set X coordinates
        :param value: Integer
        """
        if self.x == value:
            return

        self._x = value

        if self.parent:
            self.parent.updatePosition()

    @property
    def width(self) -> int:
        """
        Get the width of the component
        :return: Integer
        """
        return self._width

    @width.setter
    def width(self, value: int):
        """
        Set the width of the component
        :param value: Integer
        """
        if self.width == value:
            return

        self._width = value

        if self.parent:
            self.parent.updatePosition()

    @property
    def y(self) -> int:
        """
        Y coordinates
        :return: Integer
        """
        return self._y

    @y.setter
    def y(self, value: int):
        """
        Set Y coordinates
        :param value: Integer
        """
        if self.y == value:
            return

        self._y = value

        if self.parent:
            self.parent.updatePosition()

    @property
    def height(self) -> int:
        """
        Height of the component
        :return: Integer
        """
        return self._height

    @height.setter
    def height(self, value: int):
        """
        Set the height of the component
        :param value: Integer
        """
        if self.height == value:
            return

        self._height = value

        if self.parent:
            self.parent.updatePosition()
