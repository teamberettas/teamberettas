import pyglet
from gamelib import constants

class BaseItem(pyglet.sprite.Sprite):
    IMAGE = None
    WEIGHT = 1 

    def __init__(self):
        img = pyglet.resource.image(self.IMAGE)
        pyglet.sprite.Sprite.__init__(self, img)
        
    def get_abs(self, strDim):
        return getattr(self, strDim) - getattr(self.image, "anchor_%s" % strDim)
        
    def clear(self):
        self.batch = self.group = None
        
    def tick(self, dt):
        pass
    
