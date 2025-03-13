from flight_deck.flight_deck_component.component import Component, ComponentName


@ComponentName("br")
class Break(Component):
    """
    Break class
    Mainly for spacing purpose
    """

    def __init__(self, **kwargs):
        super().__init__(height=1, **kwargs)
