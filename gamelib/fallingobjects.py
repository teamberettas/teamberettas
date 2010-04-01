import pyglet, math
from gamelib.baseitem import BaseItem

class BaseFallingObject(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)
        self.Speed = 30
        self.image.anchor_x = self.width/2
        self.image.anchor_y = self.height/2
        
    def tick(self, dt):
        self.y -= self.Speed * 10 * dt

class FallingPaper(BaseFallingObject):
    IMAGE = "box_paper.png"
    
class FallingWood(BaseFallingObject):
    IMAGE = "box_wood.png"

class FallingRock(BaseFallingObject):
    IMAGE = "box_stones.png"
