import pyglet
from gamelib.baseitem import BaseItem

class Teeter(BaseItem):
    def __init__(self):
        BaseItem.__init__(self, "menubullet.png")
        self.position = (300, 0)

    def tick(self, dt):
        pass
    
