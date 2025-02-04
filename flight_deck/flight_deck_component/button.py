from typing import Callable

from flight_deck.flight_deck_component.base_component import BaseComponent


class ButtonComponent(BaseComponent):

    _flight_deck_component_name = "button"

    click: Callable

    def __init__(self, click: Callable, **kwargs):
        super().__init__(**kwargs)
        self.click = click