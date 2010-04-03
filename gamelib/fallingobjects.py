import pyglet, math
from gamelib.baseitem import BaseItem

class BaseFallingObject(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)
        self.Gravity = 10
        self.Speed = self.Gravity * self.WEIGHT
        self.IsFalling = True
        self.LastYDelta = 0
        
    def Land(self):
        self.IsFalling = False

    def tick(self, dt):
        if self.IsFalling:
            dy = self.Speed * dt
            self.y -= dy
            self.LastYDelta = dy

class FallingPaper(BaseFallingObject):
    IMAGE = "box_paper.png"
    WEIGHT = 10

class FallingWood(BaseFallingObject):
    IMAGE = "box_wood.png"
    WEIGHT = 20 

class FallingRock(BaseFallingObject):
    IMAGE = "box_stones.png"
    WEIGHT = 40

class FallingBaby(BaseFallingObject):
    IMAGE = "baby.png"
    WEIGHT = 25

class FallingBanana(BaseFallingObject):
    IMAGE = "bananas.png"
    WEIGHT = 15

class FallingCar(BaseFallingObject):
    IMAGE = "car.png"
    WEIGHT = 60

class FallingNoFire(BaseFallingObject):
    IMAGE = "nofire.png"
    WEIGHT = 30

class FallingSombrero(BaseFallingObject):
    IMAGE = "sombrero.png"
    WEIGHT = 5

class NullItem(BaseItem):
    IMAGE = "null_item.png"
