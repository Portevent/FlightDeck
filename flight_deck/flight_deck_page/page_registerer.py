from typing import Callable
from xml.etree import ElementTree


def FlightDeckPage(content: str) -> Callable:

    def wrapper(cls):
        cls._flight_deck_page_tree = ElementTree.fromstring(content)

        return cls

    return wrapper