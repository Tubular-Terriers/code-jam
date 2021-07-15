class Event:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eq(self, name):
        return self.name == name
