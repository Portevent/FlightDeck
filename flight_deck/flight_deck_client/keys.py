class FlightKey:

    special: bool
    key: str
    
    def __init__(self, special: bool, key: str):
        self.special = special
        self.key = key

    @staticmethod
    def text(content: str) -> 'FlightKey':
        return FlightKey(False, content)

    @staticmethod
    def special(name: str) -> 'FlightKey':
        return FlightKey(True, name)