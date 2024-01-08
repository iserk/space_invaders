from collections import namedtuple


Sprite = namedtuple("Sprite", ["frames", "width", "height"])


class GameObject:
    def __init__(self, scene):
        self.scene = scene
        self.scene.add_object(self)
        self.destroyed = False

    def draw(self, camera):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        """Returns True if the event was not handled and should be passed to the next object"""
        return True

    def destroy(self):
        self.destroyed = True

    def __repr__(self):
        return f"{self.__class__.__name__}<{id(self)}>)"
