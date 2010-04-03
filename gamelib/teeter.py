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
        self.position = (constants.RESOLUTION[0]/2, 100)

    def tick(self, dt):
        if abs(self.rotation) < 90:
            self.angularVelocity += self.getForce()
            self.rotation += self.angularVelocity * dt
            
        # Adjust the angle of the objects on the teeter.
        settleSpeed = 30
        for distance, obj in self.Objects:
            angleOffset = self.rotation - obj.rotation
            sign = angleOffset / abs(angleOffset)
            # Don't over-adjust "into" the teeter; the max adjustment is the total difference.
            adjustment = min(settleSpeed * dt, abs(angleOffset))
            obj.rotation += adjustment * sign
            
    def getAngle(self, offset=0):
        # Pyglet handles rotation degrees (and apparently 90* offset ones) while math like radians.
        return (math.pi / 180) * (self.rotation - offset)
            
    def getTopPoints(self):
        theta = self.getAngle(offset=270)
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
        
        intersects = ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
        
        # Above method doesn't work well if the teeter is very close to parallel since the lines may completely pass each other in a tick.
        if not intersects and abs(self.rotation) < 15:
            selfx, selfy = self.get_abs_pos()
            objx, objy = obj.get_abs_pos()
            # Did the object just cross the teeter?
            if objy < self.y and objy + obj.LastYDelta >= self.y:
                if objx + obj.width > self.y and objx < selfx + self.width:
                    intersects = True
        
        return intersects

    def getForce(self):
        """
        Get the net force exerted on the teeter.
        Negative force is to the left of center, positive to the right.
        """
        force = 0
        # A number to multiply the weight by to make the teeter totter just right.
        forceScalar = 0.1
        for distance, obj in self.Objects:
            leverage = distance / (self.width/2)
            force += leverage * self.WEIGHT * forceScalar
        return force
    
    def hold(self, itemObject):
        # Figure out which point on the object collided, and anchor it there.
        abs_x, abs_y = itemObject.get_abs_pos()
        anchor = 0
        multiplier = 1
        if self.rotation < 0:
            # It was the right side that collided
            anchor += itemObject.width
            
        if self.rotation % 360 == 0:
            distance = abs_x - self.x # + itemObject.width/2
        else:
            dy = abs_y - self.y
            distance = dy / math.sin(self.getAngle(180))
            
        self.Objects.append([distance, itemObject])
        # Inform the item it has landed.
        itemObject.Land()
        itemObject.image.anchor_y = 0
        itemObject.image.anchor_x = anchor
        
    def draw(self):
        theta = self.getAngle()
        for distance, item in self.Objects:
            x, y = self.position
            dx = math.cos(theta) * distance
            dy = math.sin(theta) * distance
            item.position = (x+dx, y-dy)
            item.draw()
        BaseItem.draw(self)
