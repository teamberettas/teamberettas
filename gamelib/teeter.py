import pyglet, math
from gamelib import constants
from gamelib.baseitem import BaseItem

class Teeter(BaseItem):
    IMAGE = "teeter.png"
    def __init__(self):
        BaseItem.__init__(self)
        self.Objects = []
        self.angularVelocity = 0
        self.image.anchor_x = self.width/2
        self.image.anchor_y = self.height
        self.position = (constants.RESOLUTION[0]/2, 50)

    def tick(self, dt):
        if abs(self.rotation) < 90:
            self.angularVelocity += self.getForce()
            self.rotation += self.angularVelocity * dt
            
    def getTopPoints(self):
        theta = (math.pi / 180) * (self.rotation - 90)
        omega = self.width / 2
        
        dx = math.sin(theta) * omega
        dy = math.cos(theta) * omega
        a = (self.x - dx, self.y - dy)
        b = (self.x + dx, self.y + dy)
        return a, b
            
    def intersects(self, obj):
        # Figure out if the object is landing on the teeter, based on line intersection:
        # Does the bottom of the object intersect with the angled line of the top of the teeter?
        def ccw((ax,ay), (bx,by), (cx,cy)):
            return (cy-ay)*(bx-ax) > (by-ay)*(cx-ax)
        
        A = (obj.x - obj.image.anchor_x, obj.y - obj.image.anchor_y)
        B = (A[0] + obj.width, A[1])
        C, D = self.getTopPoints()
        
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def getForce(self):
        """
        Get the net force exerted on the teeter.
        Negative force is to the left of center, positive to the right.
        """
        force = -.05
        return force
        for obj in self.Objects:
            leverage = obj.relative_x / (self.width / 2)
            force += leverage
    
    def hold(self, itemObject):
        self.Objects.append(itemObject)
        
    def draw(self):
        for item in self.Objects:
            item.draw()
        BaseItem.draw(self)
