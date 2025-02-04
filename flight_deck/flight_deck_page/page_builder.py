from typing import Type
from xml.etree.ElementTree import Element

from flight_deck.flight_deck_client.base_client import FlightDeckBaseClient
from flight_deck.flight_deck_component.base_component import BaseComponent


class PageBuilder:

    @staticmethod
    def instantiate(page: Type[BaseComponent], client: FlightDeckBaseClient) -> BaseComponent:
        return PageBuilder.__instantiate_element(page(), page._flight_deck_page_tree, client)

    @staticmethod
    def __instantiate_element(page: BaseComponent, element: Element, client: FlightDeckBaseClient):
        return client.getComponent(element.tag)(
            content=
                 [PageBuilder.__instantiate_element(page, child, client) for child in element]
                 + ([element.text] if element.text.strip() else []),
                 **PageBuilder.__parse_attributes(element.attrib, page)
        )


    @staticmethod
    def __parse_attributes(attributes, page: any):
        for key in attributes:
            if len(attributes[key]) == 0:
                continue
            if attributes[key][0] == "@":
                attributes[key] = getattr(page, attributes[key][1:])

        return attributes