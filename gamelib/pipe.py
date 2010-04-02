import pyglet, math
from gamelib import constants
from gamelib.baseitem import BaseItem

class Pipe(BaseItem):
    IMAGE = "pipe.png"
    def __init__(self):
        BaseItem.__init__(self)
        self.Objects = []
        self.image.anchor_x = self.width/2
        self.image.anchor_y = self.height
        self.position = (constants.RESOLUTION[0]/2, constants.RESOLUTION[1])
	
	self.counter = 0;
	self.xcontrol = constants.RESOLUTION[0]/2

    def tick(self, dt):
        #x = sine function of tick-based counter and screen width
        self.counter++
        self.xcontrol = (math.sin(self.counter * math.pi / 15) * constants.RESOLUTION[0] / 2) + (constants.RESOLUTION[0] / 2)

        if self.counter > 30:
            self.counter = 0
    
    def draw(self):
        self.position = (self.xcontrol, constants.RESOLUTION[1])
        BaseItem.draw(self)
