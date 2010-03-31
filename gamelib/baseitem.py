import pyglet
from gamelib import constants

class BaseItem(pyglet.sprite.Sprite):
    NAME = None
    IMAGE = None
    def __init__(self):
        pyglet.sprite.Sprite.__init__(self, self.IMAGE)
        #self.scale = 2.0
        
    def clear(self):
        self.batch = self.group = None
        
    def tick(self, dt):
        pass
    
