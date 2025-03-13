from abc import ABC, abstractmethod

from flight_deck.flight_deck_component.component import Component


class InteractionComponent(Component, ABC):

    def previousComponent(self):
        self.client.dom.previousComponent()

    def nextComponent(self):
        self.client.dom.nextComponent()

    @abstractmethod
    def inputChar(self, char: str):
        """
        Character is inputted in the field
        :param char: Inputed char
        """
        raise NotImplementedError

    @abstractmethod
    def goLeft(self):
        """
        Going left is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def goRight(self):
        """
        Going right is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def goUp(self):
        """
        Going up is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def goDown(self):
        """
        Going down is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def enter(self):
        """
        Enter key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def goStart(self):
        """
        Start key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def goEnd(self):
        """
        End key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        """
        Delete key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def suppr(self):
        """
        Suppr key is inputted in the field
        """
        raise NotImplementedError

    @abstractmethod
    def select(self):
        """
        Field is being selected
        """
        raise NotImplementedError

    @abstractmethod
    def unselect(self):
        """
        Field is being unselected
        """
        raise NotImplementedError