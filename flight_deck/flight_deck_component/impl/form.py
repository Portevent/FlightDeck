from flight_deck.flight_deck_component.component import Component, ComponentName
from flight_deck.flight_deck_component.interaction_component import InteractionComponent
from flight_deck.flight_deck_component.field import Field


@ComponentName("form")
class FormComponent(Component):

    def getFormValues(self):
        values = {}
        for component in self.iterOverChildren():
            if isinstance(component, Field):
                values[component.name] = component.value
        
        return values
