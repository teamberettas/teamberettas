import pyglet
from gamelib.baseitem import BaseItem

class Teeter(BaseItem):
    def __init__(self):
        BaseItem.__init__(self, "teeter.png")
        self.position = (400-self.width/2, 0)

    def tick(self, dt):
        pass
    
