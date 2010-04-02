import pyglet, math
from gamelib.baseitem import BaseItem

class BaseFallingObject(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)
        self.Gravity = 10
        self.Speed = self.Gravity * self.weight

    def tick(self, dt):
        self.y -= self.Speed * dt

class FallingPaper(BaseFallingObject):
    IMAGE = "box_paper.png"
    weight = 10

class FallingWood(BaseFallingObject):
    IMAGE = "box_wood.png"
    weight = 20 

class FallingRock(BaseFallingObject):
    IMAGE = "box_stones.png"
    weight = 40
