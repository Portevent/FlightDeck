from abc import abstractmethod

from flight_deck.flight_deck_component.component import Input, Template
from flight_deck.flight_deck_component.impl.text import TextComponent
from flight_deck.flight_deck_component.interaction_component import InteractionComponent

@Input("name")
@Input("label")
@Input("value")
@Template("""<Template>
<text id="label" x=0 y=0 text='@formatedLabel'/><text id="value" x=10 y=0 text='@formatedValue'/>
</Template>""")
class Field(InteractionComponent):
    """
    Component that has an instance name, a label and a value
    Note : Do not confuse Component's name with Field's name. Component's name is "Field", Field's name is whatever
    the instance have, and represent business logic
    E.G. : name : "requester_name", label : "Your name", value : "PPORTE"
    name : "age", label : "Age", value: 25
    """

    current_size: int = 0  # Size of the current value


    def onInputChange(self, input: str, name: str):
        match input:
            case "label":
                self.displayLabel()
            case "value":
                self.displayValue()
            case _:
                self.display()

    @property
    def labelComponent(self) -> TextComponent:
        return self.searchChildren("label")

    @property
    def valueComponent(self) -> TextComponent:
        return self.searchChildren("value")

    def displayAfterContent(self):
        self.displayLabel()
        self.displayValue()

    @abstractmethod
    def displayLabel(self):
        raise NotImplementedError

    @abstractmethod
    def displayValue(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def formatedLabel(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def formatedValue(self) -> str:
        raise NotImplementedError