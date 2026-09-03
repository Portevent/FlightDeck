class ContentIterator:

    def __init__(self, component):
        self.component = component

    def __iter__(self):
        yield from self.iterOver(self.component)

    def iterOver(self, component):
        yield component
        for child in component.get_content():
            yield from self.iterOver(child)
