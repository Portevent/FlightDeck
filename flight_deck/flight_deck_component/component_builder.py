from typing import Type, Dict, Tuple, List
from xml.etree.ElementTree import Element

from flight_deck.flight_deck_client.base_client import FlightDeckBaseClient
from flight_deck.flight_deck_component.component import Component
from flight_deck.flight_deck_component.interaction_component import InteractionComponent


class ComponentBuilder:

    @staticmethod
    def instantiate(componentClass: Type[Component], client: FlightDeckBaseClient) -> Tuple[Component, List[Component]]:
        """
        Instantiate a component and return all selectionnable sub components
        :param component:
        :param client:
        :return:
        """
        component = ComponentBuilder.__instantiate_element(componentClass, {}, client)
        return component, [content for content in component.getContent() if isinstance(content, InteractionComponent)]

    @staticmethod
    def __instantiate_element(componentClass: Type[Component], inputs: Dict[str, any], client: FlightDeckBaseClient, **kwargs) -> Component:
        """
        Instantiate a new component
        :param componentClass: class
        :param inputs: Inputted values
        :param client: context
        :return:
        """
        instance = componentClass(inputs=inputs, client=client, **kwargs)

        if componentClass._flight_deck_template is not None:
            for element in componentClass._flight_deck_template:
                ComponentBuilder.__instantiate_content(instance, element, client)

        return instance

    @staticmethod
    def __instantiate_content(instance: Component, element: Element, client: FlightDeckBaseClient):
        """
        Insert a new content in a Component. The new content is instantiated from a Template Element
        :param instance: Instance to populate
        :param element: Template to use
        :param client: Context
        """
        instance.addContent(
            ComponentBuilder.__instantiate_element(
                componentClass=client.getComponent(element.tag),
                client=client,
                parent=instance,
                **ComponentBuilder.__parse_attributes(element.attrib, instance)
            )
        )

    @staticmethod
    def __parse_attributes(attributes, page: Component):
        arguments = {
            'inputs': {},
            'binds': []
        }

        for key in attributes:
            if len(attributes[key]) == 0:
                continue

            value = ComponentBuilder.__parse_attribute(key, attributes[key], page)

            if attributes[key][0] == '#':
                arguments['binds'].append((page, key, attributes[key][1:]))

            if key[0] == "_":
                arguments[key[1:]] = value
            else:
                arguments['inputs'][key] = value

        return arguments

    @staticmethod
    def __parse_attribute(key, value, page):
        if value[0] == "@" or value[0] == "#":
            return getattr(page, value[1:])

        return value
