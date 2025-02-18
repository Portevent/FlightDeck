from abc import ABC, abstractmethod
from typing import Type

from flight_deck.flight_deck_component.component import Input, Template, Output
from flight_deck.flight_deck_component.interaction_component import InteractionComponent

LABEL_SIZE = 10

def SetValidChar(chars: str):
    """
    Change the valid char that can be inputted into a field
    """
    def updateValidChars(cls: Type[Field]):
        cls.valid_char = chars
        return cls

    return updateValidChars

@Input("name")
@Input("label")
@Input("value")
@Output("formatedSelection")
@Output("formatedLabel")
@Output("formatedValue")
@Template(f"""
<Template>
    <horizontal>
        <text id="label" text='#formatedSelection'/>
        <text id="label" _width="{LABEL_SIZE}" text='#formatedLabel'/>
        <text text='  '/>
        <text id="value" text='#formatedValue'/>
    </horizontal>
</Template>
""")
class Field(InteractionComponent, ABC):
    """
    Component that has an instance name, a label and a value
    Note : Do not confuse Component's name with Field's name. Component's name is "Field", Field's name is whatever
    the instance have, and represent business logic
    E.G. : name : "requester_name", label : "Your name", value : "PPORTE"
    name : "age", label : "Age", value: 25
    """

    valid_char = "abcdefghtijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,?;.:/|\\!*$^¨`_-=+'\"{}()[]°@&~éèàç"

    current_size: int = 0  # Size of the current value

    name: str
    label: str
    value: str

    formatedSelection: str
    formatedLabel: str
    formatedValue: str

    label_fill = "."
    value_fill = "."
    value_max_size: int

    def start(self):
        self.updateSelection()
        self.updateLabel()
        self.updateValue()

        self.value_max_size = self.getValueMaxSize()

    @abstractmethod
    def getValueMaxSize(self) -> int:
        """
        Determine the max size of the value, so it can be filled with that many "self.value_fill" characters
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def newChar(self, char: str):
        """
        A valid key is pressed
        """
        raise NotImplementedError

    def inputChar(self, char: str):
        if char in self.valid_char:
            self.newChar(char)

    def onInputChange(self, input: str, value: str):
        match input:
            case "label":
                self.updateLabel()
            case "value":
                self.updateValue()
            case _:
                self.display()

    def updateLabel(self):
        """
        Update the displayed label
        """
        self.formatedLabel = self.textOver(self.value, self.label_fill, LABEL_SIZE)

    def updateValue(self):
        """
        Update the displayed label
        """
        self.formatedValue = self.textOver(self.value, self.value_fill, self.value_max_size)

    def textOver(self, text: str, background: str = "_", background_lenght: int = 10) -> str:
        return text + (background * background_lenght)[len(text):]

    def updateSelection(self, selected: bool = False):
        self.formatedSelection = "> " if selected else "  "

    def select(self):
        self.updateSelection(True)

    def unselect(self):
        self.updateSelection(False)

    def goUp(self):
        self.previousComponent()

    def goDown(self):
        self.nextComponent()

    def enter(self):
        self.nextComponent()
