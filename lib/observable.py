Observer = [[], None]


class Observable:

    observers: list

    def __init__(self):
        self.observers = []

    def __del__(self):
        self.observers.clear()

    def observe(self, observer: Observer):
        self.observers.append(observer)

    def fire(self, *args):
        for observer in self.observers:
            observer(*args)
