import pyglet, math
from gamelib.baseitem import BaseItem

class Teeter(BaseItem):
    def __init__(self):
        BaseItem.__init__(self, "teeter.png")
        self.Objects = []
        self.angularVelocity = 0
        self.image.anchor_x = self.width/2
        self.image.anchor_y = self.height/2
        self.position = (400, 50)

    def tick(self, dt):
        if math.fabs(self.rotation) < 90:
            self.angularVelocity += self.getForce()
            self.rotation += self.angularVelocity

    def getForce(self):
        """
        Get the net force exerted on the teeter.
        Negative force is to the left of center, positive to the right.
        """
        force = -.001
        for obj in self.Objects:
            leverage = obj.relative_x / (self.width / 2)
            force += leverage
        return force

    
