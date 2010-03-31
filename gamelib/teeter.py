import pyglet
from gamelib.baseitem import BaseItem

class Teeter(BaseItem):
    IMAGE = pyglet.resource.image("menubullet.png")

    def __init__(self):
        BaseItem.__init__(self)
        self.position = (300, 0)

    def tick(self, dt):
        pass
    
