from flight_deck.flight_deck_component.component import Component, ComponentName


@ComponentName("logo")
class Logo(Component):
    """
    Logo
    """

    def __init__(self, **kwargs):
        super().__init__(height=3, width=6, **kwargs)

    def displayAfterContent(self):
        self._displayText(["//--\\\\",
                           "||  ||",
                           "\\\\__//"])
