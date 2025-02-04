class DeckFlightException(Exception):
    pass


class DeckFlightGivenIncorrectComponentException(DeckFlightException):
    pass


class DeckFlightAlreadyHasComponentException(DeckFlightException):
    pass
