class FlightDeckException(Exception):
    pass


class FlightDeckGivenIncorrectComponentException(FlightDeckException):
    pass


class FlightDeckAlreadyHasComponentException(FlightDeckException):
    pass
